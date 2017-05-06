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
        'Adj' : ['green', 'blue', 'illiterate', 'cheerful', 'elated', 'ethereal,' 'transliterated', 'randy', 'greasy'],
        'SingNoun' : ['duck', 'ant', 'egg', 'window', 'cereal', 'AI project', 'ulna', 'trenchcoat', 'denture'],
        'SingPropNoun' : ['Jack', 'Jill', 'Fred', 'George', 'Doris', 'Illuminati', 'Big Brother', 'Arcady Ivanovich'],
        'AdvPlace' : ['here', 'there', 'everywhere'],
        'AdvTimePres' : ['today', 'Friday', 'this week', 'sometime'],
        'AdvTimePast' : ['yesterday', 'last Wednesday', 'last month']
    }

    skeleton_gram_str = ''.join(open('species2.pcfg'))

    for w in wordbank.keys():
        skeleton_gram_str = addterminals(skeleton_gram_str, w, wordbank[w])

    return skeleton_gram_str, wordbank


