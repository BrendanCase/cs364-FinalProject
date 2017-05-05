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

def main():
    walt = nltk.pos_tag(gutenberg.words('whitman-leaves.txt'))
    skeleton_gram_string = ''.join(open('species1.pcfg'))

    skeleton_gram_string = addterminals(skeleton_gram_string, 'Det', ['the', 'a', 'this', 'all' 'each', 'another', 'any'])
    skeleton_gram_string = addterminals(skeleton_gram_string, 'Ord', ['first', 'last', 'second', 'next', 'other'])
    skeleton_gram_string = addterminals(skeleton_gram_string, 'Adj', sample(set(
        [word for (word, tag) in walt
        if tag == 'JJ' and len(word) > 3]
        ), 25))
    skeleton_gram_string = addterminals(skeleton_gram_string, 'SingNoun', sample(set(
        [word for (word, tag) in walt
        if tag == 'NN' and len(word) > 3]
        ), 40))
    skeleton_gram_string = addterminals(skeleton_gram_string, 'SingPropNoun', ['Joe', 'Jake', 'Brendan', 'Adam Eck'])
    skeleton_gram_string = addterminals(skeleton_gram_string, 'Prep', ['on', 'in', 'over', 'through', 'around', 'like'])
    skeleton_gram_string = addterminals(skeleton_gram_string, 'PersPro', ['he', 'she', 'they', 'it'])
    skeleton_gram_string = addterminals(skeleton_gram_string, 'PosPro', ['him', 'her', 'my', 'them', 'it'])
    skeleton_gram_string = addterminals(skeleton_gram_string, 'LV', ['appears', 'becomes', 'grows', 'smells', 'sounds', 'tastes', 'feels', 'remains'])

    prod = Producer('/u/_junebug_', skeleton_gram_string)

    for i in range(10):
        print(prod.parent_grammar.get_post())



if __name__ == '__main__':
    main()

