'''
combining_sents.py
illustrates a few different ways different independent clause (species) can be
joined together to make a more interesting sentence. This opens up for more
diverse and meaningful crossover mutations
'''

from producer_class import addterminals
from producer_class import Producer
import nltk
import environment

def main():
    wordbank2 = {
        'Det' : ['the', 'this', 'that', 'each', 'every', 'another'],
        'Ord' : ['first', 'second', 'last', 'middle', 'third', 'final', 'penultimate'],
        'Adj' : ['green', 'blue', 'illiterate', 'cheerful', 'elated', 'ethereal,' 'transliterated', 'randy', 'greasy'],
        'SingNoun' : ['duck', 'ant', 'egg', 'window', 'cereal', 'AI project', 'ulna', 'trenchcoat', 'denture'],
        'SingPropNoun' : ['Jack', 'Jill', 'Fred', 'George', 'Doris', 'Illuminati', 'Big Brother', 'Arcady Ivanovich'],
        'AdvPlace' : ['here', 'there', 'everywhere'],
        'AdvTimePres' : ['today', 'Friday', 'this week', 'sometime'],
        'AdvTimePast' : ['yesterday', 'last Wednesday', 'last month']
    }

    wordbank3 = {
        'Det' : ['the', 'this', 'that', 'every', 'another', 'a single'],
        'Ord' : ['fourth', 'eleventh', 'last', 'middle', 'third', 'final', 'penultimate'],
        'Adj' : ['red', 'blue', 'winning', 'cheerful', 'elated', 'big', 'little', 'scared', 'rare', 'mucosal', 'phallic'],
        'SingNoun' : ['spider', 'bucket', 'steak', 'milk', 'computer', 'snowman', 'milksteak', 'funnel', 'babycarrot'],
        'SingPropNoun' : ['Brendan', 'Ed', 'Jimmy', 'Hannah', 'Ryan', 'Helena', 'Svetlana', 'Pamela', 'Vladimir'],
        'AdvDeg' : ['very', 'mostly', 'rarely', 'never']
    }

    skeleton_gram_str2 = ''.join(open('species2.pcfg'))

    skeleton_gram_str3 = ''.join(open('species3.pcfg'))

    for w in wordbank2.keys():
        skeleton_gram_str2 = addterminals(skeleton_gram_str2, w, wordbank2[w])

    for w in wordbank3.keys():
        skeleton_gram_str3 = addterminals(skeleton_gram_str3, w, wordbank3[w])

    user1 = environment.User('/u/_junebug_', None, True, None, True)
    prod1 = Producer(user1, skeleton_gram_str2, wordbank2)
    user1.producer = prod1
    user2 = environment.User('/u/_gstring_', None, True, None, True)
    prod2 = Producer(user2, skeleton_gram_str3, wordbank3)
    user2.producer = prod2
    user1.buddies = [user2]
    user2.buddies = [user1]

    ##### Mutate Tests #####
    # for i in range(100):
    #     prod1.parent_grammar.mutate_weights()
    #     prod2.parent_grammar.mutate_weights()
    # print(prod1.parent_grammar.grammar)
    # print('_----------_')
    # print(prod2.parent_grammar.grammar)

    # for i in range(30):
    #     prod1.parent_grammar.add_new([prod1.parent_grammar._getnewword()])
    # prod1.parent_grammar.mutate_weights()
    # print(prod1.parent_grammar.grammar)

    # for i in range(100):
    #     bw = prod2.parent_grammar._getbudword(user1.producer)
    #     if bw is not None:
    #         prod2.parent_grammar.add_new([bw])
    # prod2.parent_grammar.mutate_weights()
    # print(prod2.parent_grammar.grammar)

    # prod1.parent_grammar.merge(prod1.parent_grammar._getsep(), prod2)
    # print(prod1.parent_grammar.grammar)
    #
    # print(prod1.wordlist)

    for i in range(100):
        prod1.parent_grammar.mutate()
        prod2.parent_grammar.mutate()

    print(prod1.parent_grammar.grammar)
    print('_----------_')
    print(prod2.parent_grammar.grammar)

    for i in range(10):
        print(prod1.parent_grammar.get_post())
        print()
        print(prod2.parent_grammar.get_post())
        print()







if __name__ == '__main__':
    main()