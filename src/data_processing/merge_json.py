#merging JSON processed texts together.

from argparse import ArgumentParser
from sys import argv
import json


def parse(args):
    parser = ArgumentParser()
    parser.add_argument("--files", help="source JSON files", nargs="*")
    parser.add_argument("--out", help="output JSON file")
    return parser.parse_args(args)

def run(args):
    out_dict = {}
    for jsonfile in args.files:
        with open(jsonfile, 'r') as j:
            out_dict.update(json.load(j))

    with open(args.out, 'w') as jout:
        json.dump(out_dict, jout)

    print "merged files saved to {}".format(args.out)

if __name__=="__main__":
    run(parse(argv[1:]))
