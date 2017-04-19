#merging JSON processed texts together.

from argparse import ArgumentParser
from sys import argv
import json


def parse(args):
    parser = ArgumentParser()
    parser.add_argument("--files", help="source JSON files", nargs="*")
    parser.add_argument("--strip_annotations", help="strip annotations/lemmatization from documents", action="store_true")
    parser.add_argument("--out", help="output JSON file")
    return parser.parse_args(args)

def run(args):
    out_dict = {}
    for jsonfile in args.files:
        with open(jsonfile, 'r') as j:

            data = json.load(j)

            if args.strip_annotations:
                #check if annotations present, i.e. element of value is a list/tuple
                #TODO: handle partially annotated corpora
                if type(data.values()[0][0]) is list or type(data.values()[0][0]) is tuple:
                    data = {key:[v[0] for v in value] for key, value in data.iteritems()}
            out_dict.update(data)

    with open(args.out, 'w') as jout:
        json.dump(out_dict, jout)

    print "merged files saved to {}".format(args.out)

if __name__=="__main__":
    run(parse(argv[1:]))
