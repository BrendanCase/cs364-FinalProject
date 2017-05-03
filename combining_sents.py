'''
combining_sents.py
illustrates a few different ways different independent clause (species) can be
joined together to make a more interesting sentence. This opens up for more
diverse and meaningful crossover mutations
'''

import nltk
from nltk.corpus import gutenberg
from random import sample
from producer_class import addterminals
from producer_class import Producer

def main():
    rules1 = [
        ('Det', ['the', 'this', 'that', 'each', 'every', 'another']),
        ('Ord', ['first', 'second', 'last', 'middle', 'third', 'final', 'penultimate']),
        ('Adj', ['green', 'blue', 'winning', 'cheerful', 'elated', 'quiet']),
        ('SingNoun', ['duck', 'ant', 'egg', 'window', 'cereal', 'AI project']),
        ('SingPropNoun', ['Jack', 'Jill', 'Fred', 'George']),
        ('VintPast', ['disappeared', 'agreed', 'waited']),
        ('VintPres', ['vanishes', 'eats', 'stands']),
        ('VintFut', ['will appear', 'will live', 'will prevail']),
        ('Adverb', ['quickly', 'properly', 'sneakily'])
    ]

    rules2 = [
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

    skeleton_gram_str1 = ''.join(open('species4.pcfg'))

    skeleton_gram_str2 = ''.join(open('species2.pcfg'))

    for r in rules1:
        skeleton_gram_str1 = addterminals(skeleton_gram_str1, r[0], r[1])

    for r in rules2:
        skeleton_gram_str2 = addterminals(skeleton_gram_str2, r[0], r[1])

    prod1 = Producer('/u/_junebug_', skeleton_gram_str1)
    prod2 = Producer('/u/_gstring_', skeleton_gram_str2)

    prod1.parent_grammar.merge(',', 'and', prod2.parent_grammar.grammar)

    for i in range(10):
        print(prod1.parent_grammar.get_post())



if __name__ == '__main__':
    main()