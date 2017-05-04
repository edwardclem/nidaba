#!/bin/bash

train=data/processed/etcsl/etcsl_train.txt
test=data/processed/etcsl/etcsl_test.txt

python src/pos_rulebased.py --train $train --test $test
