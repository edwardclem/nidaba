#very simple POS tagger, recognizing finite verbs from lexicon (gained from training data)
#and some rule-based

from argparse import ArgumentParser
import json
import re
from sys import argv
from data_processing import data_utils as dat

def parse(args):
    parser = ArgumentParser()
    parser.add_argument('--train', help="training data")
    parser.add_argument('--test', help='test data')
    return parser.parse_args(args)

#list of rules for recognizing finite verbs:
#trial and error

class POS_Rulebased:
    conjugation_prefixes = [r'mu-.*?$', r'im-ma-.*?', r'ba-.*?$', r'he2-.*?$']

    def __init__(self, train_path, test_path):
        '''
        Initializes POS tagger with training and test set.
        '''

        #load files from paths
        self.train = dat.load_tagged(train_path)
        self.test = dat.load_tagged(test_path)

        #compute total number of test tags

        self.total_test = sum([sum([1 for word, tag in line]) for line in self.test])


    def fit(self):
        '''
        Gets lexicon from training data.
        '''
        self.lexicon = {} #lexicon as hashmap
        for line in self.train:
            for word, tag in line:
                self.lexicon[word] = tag


        print "{} unique words in lexicon".format(len(self.lexicon.keys()))



    def eval(self, use_tagger='lexicon'):
        '''
        Evaluates tagger on test data.
        '''

        test_hat = []
        num_correct = 0

        for line in self.test:
            words = [word for word, tag in line]
            tags = [tag for word, tag in line]
            if use_tagger == 'lexicon':
                tags_hat = self.pos_tag_lexicon(words)
            elif use_tagger == 'unigram':
                tags_hat = self.pos_tag_unigram(words)
            num_correct +=  sum([int(tag == tag_hat) for tag, tag_hat in zip(tags, tags_hat)])

        accuracy = float(num_correct)/self.total_test

        print "accuracy with {} tagger: {}".format(use_tagger, accuracy)


    def pos_tag_lexicon(self, line):
        '''
        Tags using only lexicon.
        Line is a list of strings, returns list of tuples.
        '''

        tags = [self.lexicon.get(word, 'X') for word in line]
        return tags

    def pos_tag_unigram(self, line):
        '''
        tags line according to unigram rules and lexicon.
        '''

        tags = []

        for word in line:
            #use lexicon entry if present
            tag = self.lexicon.get(word, 'X')
            if tag == 'X':
                #retag if rules apply
                if any([re.match(pattern, word) for pattern in self.conjugation_prefixes]):
                    tag = 'VERB(F)'
            tags.append(tag)
        return tags


def run(args):
    #load lexicon and documents
    tagger = POS_Rulebased(args.train, args.test)

    tagger.fit()
    tagger.eval(use_tagger='lexicon')
    tagger.eval(use_tagger='unigram')


if __name__=="__main__":
    run(parse(argv[1:]))
