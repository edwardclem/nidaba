#!/bin/bash

script=src/data_processing/symbol_occurrences.py
xml=data/etcsl/etcsl.xml
outfolder=processed_data/cooc_single

python $script --xml $xml --out $outfolder
