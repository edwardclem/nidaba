#!/bin/bash

script=src/analysis/pmi.py
ins=processed_data/cooc_single/inst_info.feather
occ=processed_data/cooc_single/occ_info.feather

python $script --ins $ins --occ $occ --thr 25 --out results/pmi
