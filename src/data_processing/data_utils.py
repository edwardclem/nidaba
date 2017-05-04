#data processing utilities.
import random as r

r.seed(0)


#converting the ETCSL POS tags to the universal tagset
etcsl_to_universal = {'AJ':'ADJ', 'N':'NOUN', 'I':'INTJ', 'C':'CCONJ', 'AV':'ADV',
                        'V':'VERB', 'V/i':'VERB', 'V/t':'VERB', 'IP':'PRON', 'NU':'NUM',
                        'CNJ':'SCONJ', 'MA':'X', 'XP':'PRON', 'DP':'PRON', 'PD':'PRON', 'MOD':'PART',
                        'NEG':'NEG','X':'X', 'unspecified':'X'}

#loads tagged data into list of list of tuples
def load_tagged(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            all_tokens = line.split()
            tuple_list = [(all_tokens[i], all_tokens[i + 1]) for i in range(0, len(all_tokens), 2)]
            data.append(tuple_list)

    print "loaded {} lines from {}".format(len(data), filename)

    return data

#saves tagged data: list of list of tuples
#format: word TAG word TAG word TAG for each line
def save_tagged(data, out):
    output = []
    for line in data:
        line_str = ' '.join(['{} {}'.format(word.encode('utf-8'), tag.encode('utf-8')) for word, tag in line])
        #print line_str
        output.append(line_str)

    with open(out, 'w') as f:
        f.write('\n'.join(output))


    print "saved to {}".format(out)

#split data into training and testing fractions
def split_data(data, split_frac):
    #shuffle data
    r.shuffle(data)

    train_index = int(len(data)*split_frac)
    print "{} train, {} test".format(train_index + 1, len(data) - train_index + 1)
    train = data[:train_index]
    test = data[train_index:]

    return train, test
