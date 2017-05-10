#maximum entropy-based POS tagger based on NLTK

from argparse import ArgumentParser
import json
import re
from sys import argv, stdout
from data_processing import data_utils as dat
from nltk.classify import maxent
from features import feature_map

def parse(args):
    parser = ArgumentParser()
    parser.add_argument('--train', help="training data")
    parser.add_argument('--test', help='test data')
    parser.add_argument('--feature_set', help='feature sets separated by \'+\' character')
    return parser.parse_args(args)

class POS_MaxEnt:
    def __init__(self, train_path, test_path, feature_set):
        '''
        Initializes POS tagger with training and test set.
        '''

        #load files from paths
        self.train = dat.load_tagged(train_path)
        self.test = dat.load_tagged(test_path)
        print "number of word, tag pairs that appear in both train and test: {}".format(self.overlap())

        self.feature_string = feature_set

        self.feature_set = set()
        for feat in feature_set.split('+'):
            if feat in feature_map.keys():
                self.feature_set.add(feat)
            else:
                raise NameError('Feature {} invalid'.format(feat))

        if len(self.feature_set) == 0:
            raise Exception('no features provided.')

    def overlap(self):
        '''
        prints the overlap between the train and test data.
        '''

        train_unique = set()
        [[train_unique.add(pair) for pair in line] for line in self.train]

        test_unique = set()
        [[test_unique.add(pair) for pair in line] for line in self.test]

        return len(train_unique & test_unique)


    def gen_features(self, i, words, tag_history):
        '''
        generates a feature_dict for a given index in words.
        '''
        feats = {}

        for features in self.feature_set:
            feats.update(feature_map[features](i, words, tag_history))

        return feats

    def fit(self):
        '''
        Fit the model with the provided feature set.
        '''

        print "training with feature set: {}".format(self.feature_string)
        stdout.flush()
        train_toks = []

        for line in self.train:
            if len(line) > 0: #bypassing this for now
                words, tags = zip(*line)
                for i, word in enumerate(words):
                    feats = self.gen_features(i, words, tags)
                    train_toks.append((feats, tags[i]))

        #training model
        #TODO: use log-likelihood delta
        self.classifier = maxent.MaxentClassifier.train(train_toks, algorithm='GIS', max_iter=50)

    def eval(self):
        pred_tags = []
        test_tags = []

        for line in self.test:
            if len(line) > 0: #bypassing this for now
                words, tags = zip(*line)
                for i, word in enumerate(words):
                    #using predicted tags as history
                    feats = self.gen_features(i, words, pred_tags)
                    #predict tag
                    pred_tags.append(self.classifier.classify(feats))
                    test_tags.append(tags[i])

        num_correct = float(sum([1 for pred_tag, real_tag in zip(pred_tags, test_tags) if pred_tag == real_tag]))
        acc = num_correct/len(test_tags)

        print "Accuracy of MaxEnt Tagger with {} features: {}".format(self.feature_string, acc)

def run(args):
    #load lexicon and documents
    tagger = POS_MaxEnt(args.train, args.test, feature_set=args.feature_set)

    tagger.fit()
    tagger.eval()


if __name__=="__main__":
    run(parse(argv[1:]))
