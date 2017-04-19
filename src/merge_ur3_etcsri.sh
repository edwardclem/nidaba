#!/bin/bash

atfproc=data_processing/process_atf.py
mergefiles=data_processing/merge_json.py
etcsl=../data/etcsl
out=../data/processed

#merging files
python $mergefiles --files $out/ETCSRI_all_stripped.json $out/ur3.json --out $out/ur3_etcsri.json
