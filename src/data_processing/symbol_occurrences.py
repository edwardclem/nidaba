'''
Extracting symbol/imperfective morpheme co-occurence data.
Doing so for ALL verbs to get background (null hypothesis) distribution for symbols.

Produces 2 DataFrames from the ETCSL data:

V is the number of verbs in the dataset, S is the number of unique characters.

VxS binary array
    rows are verb instances
    cols are symbols, indicator if symbol appeared

Vx5 string array, containing instance information
    1st col: binary indicator, ends with -e
    2nd col: binary indicator, reduplicated
    Final 3 cols are strings:
        - full form of verb
        - Lemma of verb
        - line ID of verb
'''

from argparse import ArgumentParser
from sys import argv
from lxml import etree
import pandas as pd
import numpy as np
import re

def parse(args):
    parser = ArgumentParser()
    parser.add_argument("--xml", help="location of XML data")
    parser.add_argument("--out", help="output folder.")
    return parser.parse_args(args)


def verbs_line(line):
    '''
    Gets all verbs from a line. Returns a list of leaves.
    '''
    return [word for word in line if word.tag == 'w' and 'pos' in word.attrib and word.attrib['pos'] == 'V']

def verbs_body(body):
    '''
    Parses through a body. Sometimes a sequence of lines, sometimes sequence of divs.
    Returns a list of verbs and a list of the lines in which the verbs appeared.
    '''

    verbs = []
    line_ids = []

    for child in body:
        if child.tag == 'l':
            v = verbs_line(child)
            verbs.extend(v)
            #append the same ID to the list len(v) times.
            line_ids.extend([child.attrib['id']] * len(v))
        elif child.tag == "div1":
            for line in child:
                if line.tag == 'l':
                    v = verbs_line(line)
                    verbs.extend(v)
                    #append the same ID to the list len(v) times.
                    line_ids.extend([line.attrib['id']] * len(v))



    return verbs, line_ids

def all_verbs(root, ignore=['0', '6'], prefix="c"):
    '''
    Parses through an XML tree.
    Extracts documents that start with the provided prefix.
    Ignores documents whose second ID element is provided numbers.
    Returns a list of leaves and a list of the locations of the verbs.
    '''

    verbs = []
    line_ids = []

    for document in root:
        if 'id' in document.attrib:
            id_elems = document.attrib['id'].split(".")
            if id_elems[0] == prefix and id_elems[1] not in ignore:
                #iterate through children of document:
                #most documents contain a header and a text, both having language attribues
                for item in document:
                    if item.tag == 'text' and item.attrib['lang'] == 'sux':
                        #text should contain body
                        for child in item:
                            if child.tag == 'body':
                                v, l = verbs_body(child)
                                verbs.extend(v)
                                line_ids.extend(l)

    return verbs, line_ids


def vb_instance_info(verbs, line_ids):
    '''
    From an aligned list of verbs and their corresponding line IDs, produce
    the instance info DataFrame described above.
    '''

    #get list of all unique symbols in the dataset.
    #Symbol defined as a transliterated cuneiform character.


    forms = [vb.attrib['form'].encode('utf-8') for vb in verbs]
    lemmas = [vb.attrib['lemma'].encode('utf-8') for vb in verbs]

    #determine if each verb ends with -e, is reduplicated, both, or neither

    ends_e = np.array([1 if re.match(r'^.*e\d?$', vb.attrib['form'], flags=0) else 0 for vb in verbs])
    redup = np.array([1 if 'form-type' in vb.attrib and vb.attrib['form-type'] == 'RR' else 0 for vb in verbs] )

    df = pd.DataFrame(data={"form": forms, "lemma": lemmas, "ends_e":ends_e, "redup":redup, "line": line_ids})

    return df



def occurrance_info(verbs):
    '''
    Symbol occurance DataFrame described above.
    '''
    symbols = set()
    for verb in verbs:
        symbols.update(verb.attrib['form'].split("-"))

    print "unique symbols in verb dataset: {}".format(len(symbols))

    sym_list = list(symbols)

    #binary indicators for if verb contains symbol
    indicators = np.ndarray((len(verbs), len(sym_list)), dtype=np.int)

    for i, v in enumerate(verbs):
        for sym in v.attrib['form'].split("-"):
            sym_indx = sym_list.index(sym)
            indicators[i,sym_indx] = 1

    #create dataframe with column labels

    df = pd.DataFrame(data=indicators, columns=[sym.encode('utf-8') for sym in sym_list])
    return df

def run(args):
    print "loading data from {}".format(args.xml)

    #loads XML tree from provided file.
    #ETCSL data loads from one root XML file that loads subfiles and allows
    #traversal through individual documents.
    with open(args.xml, 'r') as f:
        #kwargs load auxilary files that enable proper parsing of the XML data
        parser = etree.XMLParser(load_dtd=True, dtd_validation=True)
        tree = etree.parse(f, parser)

    root = tree.getroot()

    verbs, line_ids = all_verbs(root)

    print "extracted {} verbs from dataset".format(len(verbs))

    inst_info = vb_instance_info(verbs, line_ids)

    occ_info = occurrance_info(verbs)

    with open("{}/instance_info.json".format(args.out), 'w') as inst_json:
        inst_json.write(inst_info.to_json())


    with open("{}/occ_info.csv".format(args.out), 'w') as occ_json:
        occ_json.write(occ_info.to_json())


if __name__=="__main__":
    run(parse(argv[1:]))
