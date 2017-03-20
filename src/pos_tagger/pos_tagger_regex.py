#very simple POS tagger, recognizing finite verbs from rules and lexicon
#input: processed lemmata/word pairs in JSON format.

from argparse import ArgumentParser
import json
import re
from sys import argv


#list of rules for recognizing finite verbs:
#trial and error
#paired with verb lexicon entry for confirmation
conjugation_prefixes = [r'mu-.*?$', r'im-ma-.*?', r'ba-.*?$']
lem_pattern = r'(?P<root>.*?)\[(?P<eng>.*?)\]'

def parse(args):
    parser = ArgumentParser()
    parser.add_argument('--lex', help="JSON containing lexicon information list")
    parser.add_argument('--docs', help="JSON containing lemmatized ATF document.")
    #TODO: save this as not a JSON?
    parser.add_argument('--out', help="output JSON containing POS tagged documents")
    return parser.parse_args(args)

#input: list of tuples (lemmatized document) and lexicon list
#output: list of tuples
#TODO: use lexicon info + lemmata for noun/adjective disambiguation + verb confirmation
def pos_tag(doc, lexicon):
    tagged_doc = []
    for word, lemmata in doc:
        if any([re.match(pattern, word) for pattern in conjugation_prefixes]):
            tagged_doc.append((word, lemmata, 'VERB'))
        else:
            tagged_doc.append((word, lemmata, 'X'))

    return tagged_doc

def run(args):
    #load lexicon and documents
    with open(args.lex, 'r') as lexfile:
        lexicon = json.load(lexfile)

    with open(args.docs, 'r') as docsfile:
        docs = json.load(docsfile)
    tagged = {name:pos_tag(doc, lexicon) for name, doc in docs.iteritems()}

    print "saving to {}".format(args.out)
    with open(args.out, 'w') as outfile:
        json.dump(tagged, outfile)

if __name__=="__main__":
    run(parse(argv[1:]))
