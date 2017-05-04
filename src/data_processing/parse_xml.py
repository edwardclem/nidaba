#parsing ETCSL TEI-XML files

from argparse import ArgumentParser
from sys import argv
from lxml import etree
import random as r
from data_utils import split_data, save_tagged, etcsl_to_universal

r.seed(0)

def parse(args):
    parser = ArgumentParser()
    parser.add_argument("--xml", help="XML file to be parsed.")
    parser.add_argument("--split", help="fraction of data used for training.", type=float)
    parser.add_argument("--out", help="location of train/test files. ")
    return parser.parse_args(args)

#returns word and part of speech tag
def parse_word(word, retag):
    x = word.attrib['form']
    if 'pos' in word.attrib:
        pos_etcsl = word.attrib['pos']
    elif word.text == 'X':
        pos_etcsl = 'X'
    #check for finite vs non-finite verbs
    #if no conjugation prefixes
    #TODO: check irregular verbs?
    if pos_etcsl == 'V' and retag:
        if word.attrib['form'].startswith(word.attrib['lemma']):
            pos = 'VERB(NF)'
        else:
            pos = 'VERB(F)'
    else:
        pos = etcsl_to_universal[pos_etcsl]
    return x, pos


def parse_text(body, retag=True):
    lines = []
    for child in body:
        if child.tag == 'l': #extracting from line
            line_data = []
            for sub in child:
                if sub.tag == 'w':
                    x, pos = parse_word(sub, retag)
                    line_data.append((x, pos))
                elif sub.tag == 'distinct' and sub.attrib['type'] == 'emesal':
                    for sub2 in sub: #words will be subordinate from distinct
                        if sub2.tag == 'w':
                            x, pos = parse_word(sub2, retag)
                            line_data.append((x, pos))
            #print line_data
            lines.append(line_data)
    return lines

#loads POS data from XML file in ETCSL format
#optionally retag non-conjugated verbs
#prefix refers to prefix of desired file type (c for transliterations, t for translations)
#ignore documents whose ID numbers start with numbers in that list
def load_xml(root_file, retag=True, prefix='c', ignore_nums=['0', '6']):
    with open(root_file, 'r') as f:
        parser = etree.XMLParser(load_dtd=True, dtd_validation=True)
        tree = etree.parse(f, parser)
    root = tree.getroot()
    all_data = []
    for document in root:
        if 'id' in document.attrib:
            id_list = document.attrib['id'].split(".")
            if id_list[0] == prefix and id_list[1] not in ignore_nums:
                #print "parsing document {}".format(document.attrib['id'])

                for child in document:
                    #check language
                    if child.attrib['lang'] == 'sux':
                        #get body of document -- may not work for proverbs
                        body = child[0] if child[0].tag == 'body' else None
                        if body is not None:
                            all_data.extend(parse_text(body))
    return all_data

def run(args):
    data = load_xml(args.xml, retag=False)

    print "total of lines: {}".format(len(data))

    print "total of words: {}".format(sum([len(line) for line in data]))

    unique = set()
    [[unique.add(word) for word in line] for line in data]
    print "unique words: {}".format(len(unique))

    train, test = split_data(data, args.split)

    save_tagged(train, args.out + "_train.txt")

    save_tagged(test, args.out + "_test.txt")


if __name__=="__main__":
    run(parse(argv[1:]))
