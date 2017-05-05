'''
species1.py
an illustration of initializing a producer with a grammar based
on species1.pcfg
'''

import nltk
from nltk.corpus import gutenberg
from random import sample
from producer_class import addterminals
from producer_class import Producer

def getGString():
    wordbank = {
    'Det': ['the', 'a', 'this', 'all' 'each', 'another', 'any'],
    'Card': ['one', 'four', 'twenty'],
    'Ord': ['first', 'last', 'second', 'next', 'other'],
    'Quant': ['many', 'few'],
    'Adj': ['smelly', 'hunky', 'smart', 'free', 'hungry', 'tasty', 'evil', 'loving'],
    'SingNoun': ['computer', 'freedom', 'cube', 'stream', 'planet', 'aventurine', 'nose', 'hunk', 'hyperbolic plane'],
    'SingPropNoun': ['Joe', 'Jake', 'Brendan', 'Adam Eck'],
    'Prep': ['on', 'in', 'over', 'through', 'around', 'like'],
    'PersPro': ['he', 'she', 'they', 'it'],
    'PosPro': ['him', 'her', 'my', 'them', 'it'],
    'LV': ['appears', 'becomes', 'grows', 'smells', 'sounds', 'tastes', 'feels', 'remains']
    }

    skeleton_gram_str = ''.join(open('species1.pcfg'))

    for w in wordbank.keys():
        skeleton_gram_str = addterminals(skeleton_gram_str, w, wordbank[w])

    return skeleton_gram_str, wordbank

