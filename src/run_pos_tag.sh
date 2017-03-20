#!/bin/bash

lexfile=../data/processed/etcsl_lexicon.json
docsfile=../data/processed/ETCSRI1_text_lemmas.json
outfile=../results/pos_tagged/ETCSRI1_tagged_rulebased.json

python pos_tagger/pos_tagger_regex.py --lex $lexfile --docs $docsfile --out $outfile
