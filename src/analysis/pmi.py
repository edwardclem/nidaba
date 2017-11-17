#calculating the Pointwise Mutual Information (PMI) between characters and the imperfective verb type
#pmi(x;y) = log(p(x,y)/(p(x)p(y)))
#modeling each character as bernoulli distribution with mean f(x)/N, f(x) is frequency and N is total number of verbs
#ranking pairs by PMI between the character and the verb type (-e, redup, both, none)
#TODO: intra-character PMI as well?

from argparse import ArgumentParser
from sys import argv
import numpy as np
import pandas as pd

def parse(args):
    parser = ArgumentParser()
    parser.add_argument("--occ", help="character occurence data feather")
    parser.add_argument("--ins", help="verb instance data feather")
    parser.add_argument("--thr", help="occurence threshold", type=int)
    parser.add_argument("--out", help="output location for results.")
    return parser.parse_args(args)


def compute_pmi(indicators, unigram_freq, inst_category, cat_freq, occ_threshold, num_instances, inst_type, outfile):
    '''
    Computes the Pointwise Mutual Information between a set of variables (columns specified by indicators)
    and the categories provided in inst_category.
    TODO: more complete documentation
    '''


    pmi_data = [] #list of pairs, containing tuples of pmi, lemma, category

    for col_id in indicators:
        #keeping the PMI for each verb category with the lemma
        data = {inst_type:col_id, "freq": unigram_freq[col_id]}
        p_l = unigram_freq[col_id]/num_instances
        for cat, cat_inds in inst_category.iteritems():
            p_c = cat_freq[cat]/num_instances
            cooc = indicators[col_id] & cat_inds
            if cooc.sum() > 0:
                p_lc = cooc.sum()/num_instances
                pmi = np.log2(p_lc/(p_l*p_c))
                h = np.log2(p_lc)
                data["{}_pmi".format(cat)] = pmi
                data["{}_cooc".format(cat)] = cooc.sum()
            else:
                # data["{}_pmi".format(cat)] = -1.0 #never occur together
                data["{}_cooc".format(cat)] = 0

        pmi_data.append(data)

    pmi_df = pd.DataFrame(pmi_data).sort_values("e_pmi",ascending=False)

    pmi_df_reordered = pmi_df[[inst_type, "freq"] + [col for col in pmi_df.columns.values if col not in [inst_type, "freq"]]]

    df_threshold = pmi_df_reordered[pmi_df_reordered['freq'] > occ_threshold]


    print "saving results to {}".format(outfile)
    df_threshold.to_csv(outfile)


def run(args):
    #TODO: maybe change data loading if this becomes annoying
    #loading data from feathers
    occ = pd.read_feather(args.occ)
    ins = pd.read_feather(args.ins)
    #first perform lemma/type PMI
    num_instances = float(len(ins)) #casting to float

    #getting unigram frequencies of each variable
    lemma_freq =  dict(ins['lemma'].value_counts())

    #computing finer-grained categories for each instance:
    #only -e, only reduplicated, both, and neither

    #converting to bool
    e = ins['ends_e'].astype('bool')

    redup = ins['redup'].astype('bool')

    #create dataFrame containing each category for each instance

    e_only = e & ~redup
    redup_only = ~e & redup
    both = e & redup
    neither = ~e & ~redup

    inst_category = {"e":e_only, "redup":redup_only, "both":both, "neither":neither}

    cat_freq = {key:val.sum() for key, val in inst_category.iteritems()}


    indicators =  pd.get_dummies(ins['lemma'])

    outstr_lemma = "{}/{}".format(args.out, "lemma_pmi.csv")
    #computing and saving lemma PMI
    compute_pmi(indicators, lemma_freq, inst_category, cat_freq, args.thr, num_instances, "lemma", outstr_lemma)

    #computing character PMI
    #first generating character counts
    char_freq = occ.sum()
    outstr_char = "{}/{}".format(args.out, "char_pmi.csv")
    compute_pmi(occ, char_freq, inst_category, cat_freq, args.thr, num_instances, "char", outstr_char)









if __name__=="__main__":
    run(parse(argv[1:]))
