#converts JSON to list of words, for debugging embedding code

from argparse import ArgumentParser
import json
from sys import argv
import io

def parse(args):
    parser = ArgumentParser()
    parser.add_argument("--json", help="json file")
    parser.add_argument("--txt", help="output text file")
    return parser.parse_args(args)

def run(args):

    with open(args.json, 'r') as f:
        data = json.load(f)

    with io.open(args.txt, 'w', encoding='utf-8') as outf:
        outstr = " ".join([" ".join(doc) for doc in data.values()])
        outf.write(outstr)


if __name__=="__main__":
    run(parse(argv[1:]))
