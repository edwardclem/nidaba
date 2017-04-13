#processing ATF files into lists of words with their corresponding lemmata
#tailored to the ATF file format used in the ETCSL corpus

from argparse import ArgumentParser
from sys import argv
import re
import json

delete_chars = ['#', '!', '<', '>', '[', ']', '...', '?', "+."]

def parse(args):
    parser = ArgumentParser()
    parser.add_argument("--atf", help="source ATF file")
    parser.add_argument("--lemmatized", help="true if the document is lemmatized", action="store_true")
    parser.add_argument("--out", help="output JSON file")
    return parser.parse_args(args)

def process_word(word, charlist):
    for char in charlist:
        word = word.replace(char, "")
    return word

#input: string containing a single ATF-formatted document, lemmatized
#output: name of document, list of tuples, containing words and their lemmatization.
def doc2seq_lemmatized(doc):
    seq = [] #list of tuples
    #first line in doc should be name
    name = doc.split("\n")[0]

    #regular expression for a line and its lemmatization, if present
    #split into group
    text_pattern = r'\n\d-?\d?\'?\.\s*(?P<text>.*?)\n#lem:\s*(?P<lem>.*?)\n'
    all_matches = re.findall(text_pattern, doc)
    for text, lem in all_matches:
        #check if line contains multiple word
        split_text = [process_word(word.strip(), delete_chars) for word in text.split()]
        if len(split_text) > 1: #multiple words
            split_lem = lem.split(';')
            #remove "+." from text
            split_lem = [word_lem.replace("+.", "").strip() for word_lem in split_lem]
            zipped = zip(split_text, split_lem) #zip corresponding words + lemmata together
            seq.extend(zipped)
        else:
            seq.append((split_text[0], lem.strip()))
    return name, seq
#input: string containing single ATF formatted document.
#NOTE: removes all lines that don't begin with a numeral (i.e. removes @column and @seal information)
#NOTE: including "seals" that aren't technically part of the main document might cause confusion.
#TODO: check language? all documents seem to be in Sumerian though
def doc2seq(doc):
    seq = [] #list of strings
    split = doc.split("\n")
    name = split[0] #first line of the document

    #removing first line
    doc = "\n".join(split[1:])


    line_pattern = r'\d-?\d?\'?\.\s*(?P<text>.*?)\s*\n' #whitespace at end of the document
    all_matches = re.findall(line_pattern, doc)

    for text in all_matches:
        split_text = [process_word(word, delete_chars) for word in text.split()]
        seq.extend(split_text)

    return name, seq

def run(args):
    with open(args.atf, 'r') as atffile:
        #join all lines together
        all_lines = "".join([line for line in atffile])

        #each document begins with & character, separate into documents
        docs = all_lines.split('&')
        #filter out empty documents
        docs = [doc for doc in docs if len(doc) > 0]

        if not args.lemmatized:
            all_seq_data = [doc2seq(doc) for doc in docs]
        else:
            all_seq_data = [doc2seq_lemmatized(doc) for doc in docs]

        #convert to dictionary, save as JSON
        data_dict = {name:document for name, document in all_seq_data}
        #save JSON

    with open(args.out, 'w') as outfile:
        json.dump(data_dict, outfile)
    print "saved to {}".format(args.out)


if __name__=="__main__":
    run(parse(argv[1:]))
