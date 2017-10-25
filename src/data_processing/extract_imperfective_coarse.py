#perform coarse extraction of imperfective data.
#returning all lines in an XML file that end with a reduplicated verb or verb that ends in "e"
#will then be filtered later by hand
from argparse import ArgumentParser
from sys import argv
from lxml import etree
from copy import deepcopy

def parse(args):
    parser = ArgumentParser()
    parser.add_argument("--xml", help="xml file to parse")
    parser.add_argument("--out", help="output text file")
    return parser.parse_args(args)

def parse_body(body):
    '''
    Parses through a body. Sometimes a sequence of lines, sometimes sequence of divs.
    '''

    lines = []

    for child in body:
        if child.tag == 'l' and is_possible_imperfective(child):
            lines.append(child)
        elif child.tag == "div1":
            for line in child:
                if line.tag == 'l' and is_possible_imperfective(line):
                    lines.append(line)

    return lines

def is_possible_imperfective(line):
    '''
    check if line contains a verb ending in -e or reduplication.
    '''

    for word in line:
        if word.tag == 'w':
            if 'pos' in word.attrib and word.attrib['pos'] == 'V':
                if 'form-type' in word.attrib and word.attrib['form-type'] == 'RR':
                    return True
                #this is the hacky way of handling -be2 kind of symbols
                if len(word.attrib['form']) >= 2:
                    if word.attrib['form'][-1] == "e" or word.attrib['form'][-2] == "e":
                        return True
    return False



def parse_xml_tree(root, ignore=['0', '6'], prefix="c"):
    '''
    Parses through an XML tree.
    Extracts documents that start with the provided prefix.
    Ignores documents whose second ID element is provided numbers.
    Returns a list of lines.
    Selects lines that contain reduplicated verbs or verbs that end with an -e.
    '''

    lines = []

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
                                lines.extend(parse_body(child))

    return lines

def save_lines(lines, outfile):

    root = etree.Element("root")

    for line in lines:
        root.append(deepcopy(line))

    treestring = etree.tostring(root, pretty_print=True)

    with open(outfile, 'w') as f:
        f.write(treestring)

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
    lines = parse_xml_tree(root)

    save_lines(lines, args.out)



if __name__=="__main__":
    run(parse(argv[1:]))
