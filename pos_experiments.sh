#!/bin/bash

train=data/processed/etcsl/etcsl_train.txt
test=data/processed/etcsl/etcsl_test.txt
out=results/pos_logs
script=src/pos_maxent.py
megam=/Users/edwardwilliams/documents/research/megam/megam #change this on different machine


# python src/pos_random.py --train $train --test $test > $out/random.txt
#
#running MaxEnt, change number of jobs depending on number of available cores
parallel -j 3 --progress --results $out/{1}_log \
python $script --train $train --test $test --megam $megam --feature_set {1} ::: morphology unigram morphology+unigram context_word context_tag context_word+context_tag context_word+context_tag+unigram context_word+context_tag+morphology context_word+context_tag+morphology

#python $script --train $train --test $test --megam $megam --feature_set morphology
