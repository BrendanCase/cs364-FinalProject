'''
species2.py
an illustration of initializing a producer with a grammar based
on species2.pcfg and making some posts
'''

import nltk
from nltk.corpus import gutenberg
from random import sample
from producer_class import addterminals
from producer_class import Producer

#def main():
def getGString():
    rules = [
        ('Det', ['the', 'this', 'that', 'each', 'every', 'another']),
        ('Ord', ['first', 'second', 'last', 'middle', 'third', 'final', 'penultimate']),
        ('Adj', ['green', 'blue', 'winning', 'cheerful', 'elated']),
        ('SingNoun', ['duck', 'ant', 'egg', 'window', 'cereal', 'AI project']),
        ('SingPropNoun', ['Jack', 'Jill', 'Fred', 'George']),
        ('Prep', ['on', 'for', 'from', 'by', 'with']),
        ('AdvPlace', ['here', 'there', 'everywhere']),
        ('AdvTimePres', ['today', 'Friday', 'this week', 'sometime']),
        ('AdvTimePast', ['yesterday', 'last Wednesday', 'last month'])
    ]

    skeleton_gram_str = ''.join(open('species2.pcfg'))

    for r in rules:
        skeleton_gram_str = addterminals(skeleton_gram_str, r[0], r[1])

    #prod = Producer('/u/_junebug_', skeleton_gram_str)

    #for i in range(10):
    #    print(prod.parent_grammar.get_post())
    return skeleton_gram_str

#if __name__ == '__main__':
#    main()

