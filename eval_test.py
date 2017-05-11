import evaluator
from length import LengthRule as L
from buddy import BuddyRule as B
from trend import TrendRule as T
from apostrophe import ApostropheRule as A
from closeword import WordRule as W
import environment
from producer_class import addterminals
from producer_class import Producer

def main():
    wordbank2 = {
        'Det': ['the', 'this', 'that', 'each', 'every', 'another'],
        'Ord': ['first', 'second', 'last', 'middle', 'third', 'final', 'penultimate'],
        'Adj': ['green', 'blue', 'illiterate', 'cheerful', 'elated', 'ethereal', 'transliterated', 'randy', 'greasy'],
        'SingNoun': ['duck', 'ant', 'egg', 'window', 'cereal', 'AI project', 'ulna', 'trenchcoat', 'denture'],
        'SingPropNoun': ['Jack', 'Jill', 'Fred', 'George', 'Doris', 'Illuminati', 'Big Brother', 'Arcady Ivanovich'],
        'AdvPlace': ['here', 'there', 'everywhere'],
        'AdvTimePres': ['today', 'Friday', 'this week', 'sometime'],
        'AdvTimePast': ['yesterday', 'last Wednesday', 'last month']
    }

    wordbank3 = {
        'Det': ['the', 'this', 'that', 'every', 'another', 'a single'],
        'Ord': ['fourth', 'eleventh', 'last', 'middle', 'third', 'final', 'penultimate'],
        'Adj': ['red', 'blue', 'winning', 'cheerful', 'elated', 'big', 'little', 'scared', 'rare', 'mucosal',
                'phallic'],
        'SingNoun': ['spider', 'bucket', 'steak', 'milk', 'computer', 'snowman', 'milksteak', 'funnel', 'babycarrot'],
        'SingPropNoun': ['Brendan', 'Ed', 'Jimmy', 'Hannah', 'Ryan', 'Helena', 'Svetlana', 'Pamela', 'Vladimir'],
        'AdvDeg': ['very', 'mostly', 'rarely', 'never']
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
    user1.evaluator = evaluator.Evaluator([A(), L(), T(), W(['spider', 'Ryan', 'Doris'], ['little', 'elated']), B(user1)], user1)
    user2.evaluator = evaluator.Evaluator([A(), L(), T(), W(['Ed', 'steak', 'never'], ['funnel', 'milk', 'green']), B(user2)], user2)

    # run 5 'iterations'
    posts = []
    for i in range(50):
        if i % 10 == 0:
            prod1.parent_grammar.mutate()
            prod2.parent_grammar.mutate()
            user1.evaluate_iteration(posts)
            user2.evaluate_iteration(posts)
            posts = []
        posts.append(prod1.parent_grammar.make_post('1', i//10))
        posts.append(prod2.parent_grammar.make_post('2', i//10))



if __name__ == '__main__':
    main()