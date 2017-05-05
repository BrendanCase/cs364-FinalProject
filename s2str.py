'''
species2.py
an illustration of initializing a producer with a grammar based
on species2.pcfg and making some posts
'''

from producer_class import addterminals

def getGString():
    wordbank = {
        'Det' : ['the', 'this', 'that', 'each', 'every', 'another'],
        'Ord' : ['first', 'second', 'last', 'middle', 'third', 'final', 'penultimate'],
        'Adj' : ['green', 'blue', 'winning', 'cheerful', 'elated'],
        'SingNoun' : ['duck', 'ant', 'egg', 'window', 'cereal', 'AI project'],
        'SingPropNoun' : ['Jack', 'Jill', 'Fred', 'George'],
        'Prep' : ['on', 'for', 'from', 'by', 'with'],
        'AdvPlace' : ['here', 'there', 'everywhere'],
        'AdvTimePres' : ['today', 'Friday', 'this week', 'sometime'],
        'AdvTimePast' : ['yesterday', 'last Wednesday', 'last month']
    }

    skeleton_gram_str = ''.join(open('species2.pcfg'))

    for w in wordbank.keys():
        skeleton_gram_str = addterminals(skeleton_gram_str, w, wordbank[w])

    return skeleton_gram_str, wordbank


