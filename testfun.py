import nltk
from nltk.corpus import brown
from nltk.corpus import gutenberg
from random import sample
import random 
import species1
import s1str
import s2str
import s3str
import s4str
import environment
from producer_class import Producer
import evaluator
from length import LengthRule
from apostrophe import ApostropheRule
from closeword import WordRule

def makeGString():
    test = Producer('/u/_junebug_', """
        S -> NP VP [1.0]
        NP -> Nom [0.7] | | Det Nom [0.2] | Pronoun [0.1]
        Nom -> Adj Nom [0.2] | Noun Nom [0.3] | Noun [0.3] | Nom PP [0.2]
        PP -> Prep NP [1.0]
        Prep -> '*' [1.0]
        Adj -> '*' [1.0]
        Pronoun -> '*' [1.0]
        Det -> '*' [1.0]
        Noun -> '*' [1.0]
        VP -> IV [0.3] | TV NP [0.3] | TV NP PP [0.2] | TV PP [0.2]
        IV -> '*' [1.0]
        TV -> '*' [1.0]""")

    test.addTerminals('Prep', ['on', 'from', 'to'])
    test.addTerminals('Adj', sample(Adjectives2, 30))
    test.addTerminals('Pronoun', sample(Pronouns, 10))
    test.addTerminals('Det', Determiners)
    test.addTerminals('Noun', sample(Nouns2, 50))
    test.addTerminals('IV', sample(IntransitiveVerbs, 10))
    test.addTerminals('TV', sample(Verbs2, 50))
    return test

def make_rand_producer(name, user, i):
    string_makers = [species1.getGString, s2str.getGString, s3str.getGString, s4str.getGString]
    #getter = random.choice(string_makers)
    print(i%4)
    getter = string_makers[i%4]
    gstring, wordlist= getter()
    producer = Producer(user, gstring, wordlist)
    return producer

def make_rand_evaluator():
    #gNums = [random.randint(0,10) for i in range(5)]
    #bNums = [random.randint(0,10) for i in range(5)]
    #wordTypes = [Adjectives2, Pronouns, Nouns2, IntransitiveVerbs, Verbs2]
    gWords = []
    bWords = []
    #for i, wtype in enumerate(wordTypes):
    #    gWords += sample(wtype, gNums[i])
    #    bWords += sample(wtype, bNums[i])
    wr = WordRule(gWords, bWords)
    #ar = ApostropheRule(random.random(), random.random(), random.random())
    #lr = LengthRule(random.random()*-1, random.random(), random.random())
    ar = ApostropheRule(random.randint(1,3), random.randint(1,3), random.randint(1,3))
    lr = LengthRule(random.randint(1,3)*-1, random.randint(1,3), random.randint(1,3))
    aEvaluator = evaluator.Evaluator([wr, ar, lr])
    return aEvaluator

def spawn_users(num, num2):
    users = []
    for i in range(num):
        name = "user_%d" % i
        user = environment.User(name, None, True, None, True)
        producer = make_rand_producer(name, user, i)
        user.producer = producer
        eva = make_rand_evaluator()
        user.evaluator = eva
        #gstring = s1str.getGString()
        #producer = Producer(name, gstring)
        #gNums = [random.randint(0,10) for i in range(5)]
        #bNums = [random.randint(0,10) for i in range(5)]
        #wordTypes = [Adjectives2, Pronouns, Nouns2, IntransitiveVerbs, Verbs2]
        #gWords = []
        #bWords = []
        #for i, wtype in enumerate(wordTypes):
        #    gWords += sample(wtype, gNums[i])
        #    bWords += sample(wtype, bNums[i])
        #wr = WordRule(gWords, bWords)
        #ar = ApostropheRule(random.random(), random.random(), random.random())
        #lr = LengthRule(random.random()*-1, random.random(), random.random())
        #aEvaluator = evaluator.Evaluator([wr, ar, lr])
        #users.append(environment.User(name, producer, True, eva, True))
        users.append(user)
    for i in range(num2):
        name = "eva_%d" % i
        producer = None
        eva = make_rand_evaluator()
        users.append(environment.User(name, producer, False, eva, True))
    return users

#ev = environment.Environment(lambda: spawn_users(10), 'test.db')
#print("setting up database")
#ev.setup_db()
#print("adding users to database")
#ev.add_users_to_db()
#for i in range(100):
#    print("on iteration %d" % i)
#    posts = ev.run_iteration
#    print("adding iteration to database")
#    ev.insert_posts(posts)


