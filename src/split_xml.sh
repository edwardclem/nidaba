#!/bin/bash

xml=../data/etcsl/etcsl.xml
out=../data/processed/etcsl/etcsl

python data_processing/parse_xml.py --xml $xml --split 0.9 --out $out
