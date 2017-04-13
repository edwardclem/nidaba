#!/bin/bash

atfproc=data_processing/process_atf.py
mergefiles=data_processing/merge_json.py
etcsl=../data/etcsl
out=../data/processed

python $atfproc --atf $etcsl/ETCSRI_RIME1.atf --out $out/ETCSRI1_text_lemmas.json --lemmatized
python $atfproc --atf $etcsl/ETCSRI_RIME2.atf --out $out/ETCSRI2_text_lemmas.json --lemmatized
python $atfproc --atf $etcsl/ETCSRI_RIME3_1.atf --out $out/ETCSRI3_1_text_lemmas.json --lemmatized
python $atfproc --atf $etcsl/ETCSRI_RIME3_2.atf --out $out/ETCSRI3_2_text_lemmas.json --lemmatized
python $atfproc --atf $etcsl/ETCSRI_RIME4.atf --out $out/ETCSRI4_text_lemmas.json --lemmatized

#merging files
python $mergefiles --files $out/ETCSRI1_text_lemmas.json \
                            $out/ETCSRI2_text_lemmas.json \
                            $out/ETCSRI3_1_text_lemmas.json \
                            $out/ETCSRI3_2_text_lemmas.json \
                            $out/ETCSRI4_text_lemmas.json \
                            --out $out/ETCSRI_all.json
