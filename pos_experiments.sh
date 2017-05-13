#!/bin/bash

train=data/processed/etcsl/etcsl_train.txt
test=data/processed/etcsl/etcsl_test.txt
out=results/pos_logs
script=src/pos_maxent.py

python src/pos_random.py --train $train --test $test > $out/random.txt

#running MaxEnt
# parallel -u --progress --results $out/{1}_log \
# python $script --train $train --test $test --feature_set {1} ::: morphology unigram morphology+unigram context_word context_tag context_word+context_tag context_word+context_tag+unigram context_word+context_tag+morphology context_word+context_tag+morphology
