#converts .glo lexicon file to list of entries in JSON format

from argparse import ArgumentParser
import json
import re
from sys import argv

def parse(args):
    parser = ArgumentParser()
    parser.add_argument("--lex", help=".glo lexicon document")
    parser.add_argument("--out", help="output JSON file with lexicon")
    return parser.parse_args(args)

#input: string with location of .glo ETCSL lexicon document.
#output: list of dictionaries, containing bases, forms, parts of speech, and senses
def process_lexicon(lexicon_file):
    #split the lexicon into entries, perform more processing on entries
    with open(lexicon_file, 'r') as lex:
        lexdata = "".join([line for line in lex])
        entry_pattern = r'@entry.*?@end?'
        entries = re.findall(entry_pattern, lexdata, flags=re.DOTALL) #enable matching newline with dot
        lexicon = [process_entry(ent) for ent in entries]
    return lexicon

#input: string describing entry in .glo files
#output:
def process_entry(entry_str):
    #extract information from entries
    entry_dict = {'forms':[]} #initializing form list
    #iterate through lines, add information if neded
    entry_pattern = r'^@entry\s*?(?P<name>.*?)\s*?\[(?P<english>.*?)\]\s*?(?P<pos>\S*?)\s*?$'
    bases_pattern = r'^@bases\s(?P<bases>.*?)$' #list of bases
    parts_pattern = r'^@parts\s(?P<parts>.*?)$'
    form_pattern = r'^@form\s+(?P<form>\S*?)\s.*?$' #NOTE: omitting analysis information

    lines = entry_str.split('\n') #splitting into lines

    #iterate through lines, check entries
    #probably a more elengant way to do this
    for line in lines:
        entry_match = re.match(entry_pattern, line)
        if entry_match:
            entry_dict['name'] = entry_match.group('name').strip()
            entry_dict['english'] = entry_match.group('english').strip()
            entry_dict['pos'] = etcsl_to_universal[entry_match.group('pos').strip()]
        else:
            bases_match = re.match(bases_pattern, line)
            if bases_match:
                entry_dict['bases'] = bases_match.group('bases').split()
            else:
                parts_match = re.match(parts_pattern, line)
                if parts_match:
                    entry_dict['parts'] = parts_match.group('parts').split()
                else:
                    form_match = re.match(form_pattern, line)
                    if form_match:
                        #get first example of form
                        form_string = form_match.group('form').split()[0]
                        #TODO: more processing on form_string probably
                        entry_dict['forms'].append(form_string)
    return entry_dict

def save_lexicon(outfile, lex):
    with open(outfile, 'w') as lexfile:
        json.dump(lex, lexfile)

def run(args):
    #loading lemmatized data
    #convert lexicon to JSON
    lex = process_lexicon(args.lex)
    print "saving to {}".format(args.out)
    save_lexicon(args.out, lex)

if __name__=="__main__":
    run(parse(argv[1:]))
