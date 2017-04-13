atfproc=data_processing/process_atf.py
out=../data/processed
ur3=../data/ur3/ur3_20110805_public.atf

python $atfproc --atf $ur3 --out $out/ur3.json
