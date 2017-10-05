#!/bin/bash

script=src/data_processing/extract_imperfective_coarse.py
xml=data/etcsl/etcsl.xml
out=processed_data/etcsl_imperfective_coarse.xml

python $script --xml $xml --out $out
