#implementation of skip-gram word embedding with Noise-Contrastive Estimation
#largely modified from the TensorFlow word2vec tutorial

import numpy as np
from argparse import ArgumentParser
import tensorflow as tf
import json
from sys import argv

def parse(args):
    parser = ArgumentParser()
    parser.add_argument("--data", help="preprocessed JSON file containing documents.")
    return parser.parse_args(args)

class SkipGram():
    def __init__(self, datapath, batch_size=128, embedding_size=128, skip_window=1, nce_samples=64, epochs=5):
        '''
        Instantiate SkipGram language model.
        '''

        self.batch_size, self.embedding_size, self.nce_samples, self.epochs = batch_size, embedding_size, nce_samples, epochs
        self.session = tf.Session() #create tensorflow session

        #load data from JSON. JSON is Dictionary where each key is a document name and
        #each value is a document, or a list of tuples (lemmatized sumerian word)
        #function returns a list of lists (stripped lemmas out)
        self.documents = self.load(datapath)

        #generate tokens for all words
        self.word2id, self.id2word = self.build_vocab(self.documents)

        self.vocab_size = len(self.id2word)



        #will create data from each document separately
        #skip is 1 for now
        self.data, self.labels = self.create_data(self.documents, skip=skip_window)

        print "number of source, context pairs: {}".format(len(self.data))

        #create placeholders
        self.train_inputs = tf.placeholder(tf.int32, shape=[self.batch_size], name="Inputs")
        self.train_labels = tf.placeholder(tf.int32, shape=[self.batch_size, 1], name="Labels")

        #create embeddings and NCE loss
        embeddings = tf.Variable(tf.random_uniform([self.vocab_size, self.embedding_size], -1.0, 1.0))
        embed = tf.nn.embedding_lookup(embeddings, self.train_inputs)

        nce_weights = tf.Variable(tf.truncated_normal([self.vocab_size, self.embedding_size], stddev=1.0 / np.sqrt(self.embedding_size)))
        nce_bias = tf.Variable(tf.zeros([self.vocab_size]))

        #create NCE loss node
        self.loss = tf.reduce_mean(tf.nn.nce_loss(weights=nce_weights,
                                                    biases=nce_bias,
                                                    labels=self.train_labels,
                                                    inputs=embed,
                                                    num_sampled=self.nce_samples,
                                                    num_classes=self.vocab_size))

        self.train_op = tf.train.AdamOptimizer(1.0).minimize(self.loss)
        self.session.run(tf.global_variables_initializer())

    def fit(self):
        '''
        Run training.
        '''
        chunk_size = (len(self.data) / self.batch_size) * self.batch_size
        for e in range(self.epochs):
            curr_loss, curr_acc, batches = 0.0, 0.0, 0.0
            #splits data into chunks
            for start, end in zip(range(0, len(self.data[:chunk_size]) - self.batch_size, self.batch_size),
                                  range(self.batch_size, len(self.data[:chunk_size]), self.batch_size)):

                loss, _ = self.session.run([self.loss, self.train_op], feed_dict={self.train_inputs: self.data[start:end],
                                                                                    self.train_labels: self.labels[start:end]})
                curr_loss, batches = curr_loss + loss, batches + 1
            print 'Epoch {} \tAverage Loss: {}\t'.format(e, curr_loss / batches)

    def load(self, datapath, lemmatized=True):
        '''
        Loads JSON file.
        '''
        with open(datapath, 'r') as f:
            string_list = json.load(f).values()
            if not lemmatized:
                return string_list
            else:
                #strip lemmas out if present
                data = []
                for l in string_list:
                    data.append([word for word, lemma in l])
                return data

    def build_vocab(self, documents):
        '''
        Produce tokens from dataset.
        Not filtering out rare words - agglutination may reduce frequency of specific tokens.
        '''
        vocab = set()
        for doc in documents:
            for word in doc:
                vocab.add(word)

        id2word = list(vocab)
        word2id = {word: i for i, word in enumerate(id2word)}

        return word2id, id2word

    def create_data(self, documents, skip=1):
        data = [] #list of tuples of tokens
        for doc in documents:
            for i, source in enumerate(doc):
                for skip_ind in range(i - skip, i + skip + 1):
                    #TODO: random sampling of context words
                    if skip_ind < len(doc) and skip_ind != i :
                        context = doc[skip_ind]
                        data.append((self.word2id[source], self.word2id[context]))

        input_data, labels = zip(*data)
        input_data = np.array(input_data, dtype=np.int32)
        labels = np.array(labels, dtype=np.int32)
        return input_data, labels.reshape(labels.shape[0], -1)


def run(args):
    sg = SkipGram(args.data)

    sg.fit() #run training

if __name__=="__main__":
    run(parse(argv[1:]))
