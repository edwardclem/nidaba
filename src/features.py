#features for POS taggers.

def morphology(i, words, tag_history):
    chars = words[i].split('-')

    feats = {}
    feats['first_char'] = chars[0]
    feats['second_char'] = "" if len(chars) == 1 else chars[1]
    feats['last_char'] = chars[-1]

    return feats

def unigram(i, words, tag_history):
    '''
    Current token features.
    '''
    feats = {}
    feats['current_word'] = words[i]
    return feats

def context_word(i, words, tag_history):
    '''
    Contextual features.
    '''
    feats = {}
    feats['prev_word'] = words[i - 1] if i > 0 else "START"
    return feats

def context_tag(i, words, tag_history):
    '''
    Tag history of word.
    '''
    feats = {}
    feats['prev_tag'] = tag_history[i - 1] if i > 0 else "START"
    return feats

feature_map = {'morphology':morphology, 'unigram':unigram,
                'context_word':context_word, 'context_tag':context_tag}
