#random POS tagger, samples from the distribution of tags
#acting as a baseline

from data_processing import data_utils as dat
from argparse import ArgumentParser
import numpy as np
from sys import argv

np.set_printoptions(suppress=True, precision=5)


def parse(args):
    parser = ArgumentParser()
    parser.add_argument('--train', help="training data")
    parser.add_argument('--test', help='test data')
    return parser.parse_args(args)

class POS_Random:
    def __init__(self, train_path, test_path):

        self.train = dat.load_tagged(train_path)
        self.test = dat.load_tagged(test_path)

    def fit(self):
        '''
        Computes the frequency of tags in the training data.
        '''

        #get list of all tags
        all_tags = []
        for line in self.train:
            all_tags.extend([tag for word, tag in line])

        self.unique, counts = np.unique(np.array(all_tags), return_counts=True)

        self.dist = counts/float(np.sum(counts))

        print "tag distributions: "

        print self.unique
        print self.dist


    def sample(self):
        '''
        samples from the categorical distribution of tags
        '''

        return np.random.choice(self.unique, p=self.dist)

    def eval(self):
        '''
        evaluate on testing data
        '''

        test_tags = []

        for line in self.test:
            if len(line) > 0:
                test_tags.extend([tag for word, tag in line])

        pred_tags = [self.sample() for tag in test_tags]


        num_correct = float(sum([1 for pred_tag, real_tag in zip(pred_tags, test_tags) if pred_tag == real_tag]))
        acc = num_correct/len(test_tags)

        print "Accuracy of Random Tagger: {}".format(acc)


def run(args):
    #load lexicon and documents
    tagger = POS_Random(args.train, args.test)

    tagger.fit()
    tagger.eval()


if __name__=="__main__":
    run(parse(argv[1:]))
