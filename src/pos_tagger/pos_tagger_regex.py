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
lem_pattern = r'(?P<root>.*?)\[(?P<eng>.*?)?\](?P<suf>.*?)$'

def parse(args):
    parser = ArgumentParser()
    parser.add_argument('--lex', help="JSON containing lexicon information list")
    parser.add_argument('--docs', help="JSON containing lemmatized ATF document.")
    #TODO: save this as not a JSON?
    parser.add_argument('--out', help="output JSON containing POS tagged documents")
    return parser.parse_args(args)

#searches through lexicon (some roots have duplicate entries) to find an entry with the corresponding root and POS
def has_lexicon_pos(root, POS, lexicon):
    for entry in lexicon:
        if entry['name'] == root and entry['pos'] == POS:
            return True
    return False

#unigram POS tagging, only using individual word construction + lexicon info
#input: list of tuples (lemmatized document) and lexicon list
#output: list of tuples, POS-tagged words
def pos_tag_unigram(doc, lexicon):
    tagged_doc = []
    for word, lemmata in doc:
        #lemmata-based preprocessing
        #remove spurious EOS markers
        lemmata = lemmata.strip("+.").strip() #TODO: fix this in the processing code? it's weird, that should have already been removed
        if lemmata =='u':
            tag = 'X'
        elif lemmata == 'n':
            tag = 'NUM'
        elif "DN" in lemmata or "PN" in lemmata or "RN" in lemmata or "TN" in lemmata or "GN" in lemmata:
            tag =  'PROPN'
        elif lemmata == "X":
            tag = 'X'
        else:
            match = re.match(lem_pattern, lemmata)
            root = match.group('root')
            if any([re.match(pattern, word) for pattern in conjugation_prefixes]):
                #search for corresponding lexicon entry - if it has a conjugation prefix and
                #is a verb in the lexicon, then it's a verb
                #cutting down on noise from words that happen to start with "mu" or "ba" etc
                #get root
                if has_lexicon_pos(root, 'VERB', lexicon):
                    tag = 'VERB'
            else:
                #if the lexicon entry is a verb but it's not conjugated, then it's a nominalized adjective
                if has_lexicon_pos(root, 'VERB', lexicon):
                    tag =  'ADJ'
                elif has_lexicon_pos(root, 'NOUN', lexicon):
                    tag = 'NOUN'
                else: #TODO: adverbs?
                    tag = 'X'

        print word, lemmata, tag
        tagged_doc.append((word, lemmata, tag))

    return tagged_doc

def run(args):
    #load lexicon and documents
    with open(args.lex, 'r') as lexfile:
        lexicon = json.load(lexfile)

    with open(args.docs, 'r') as docsfile:
        docs = json.load(docsfile)

    tagged = {name:pos_tag_unigram(doc, lexicon) for name, doc in docs.iteritems()}

    print "saving to {}".format(args.out)
    with open(args.out, 'w') as outfile:
        json.dump(tagged, outfile)

if __name__=="__main__":
    run(parse(argv[1:]))
