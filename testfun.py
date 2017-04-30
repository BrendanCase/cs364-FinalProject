import nltk
from nltk.corpus import brown
from nltk.corpus import gutenberg
from random import sample
import random 
import s1str
import environment
from producer_class import Producer
import evaluator
from length import LengthRule
from apostrophe import ApostropheRule
from closeword import WordRule

Brown = brown.tagged_words(tagset='universal')
Carroll = nltk.pos_tag(gutenberg.words('whitman-leaves.txt'))

#Adjectives1 = set([word for (word, tag) in brown.tagged_words(tagset='universal') if tag == 'ADJ'])
Adjectives2 = set(
    [word for (word, tag) in Carroll
     if tag == 'JJ' and len(word) > 3]
)
Pronouns = set([word for (word, tag) in Brown if tag == 'PRON'])
Determiners = set([word for (word, tag) in Brown if tag == 'DET'])
#Nouns1 = set([word for (word, tag) in brown.tagged_words(tagset='universal') if tag == 'NOUN'])
Nouns2 = set(
    [word for (word, tag) in Carroll
     if tag == 'NN' and len(word) > 3]
)
IntransitiveVerbs = set([w.strip('\n') for w in open('intransitives.txt')])
#Verbs1 = set([word for (word, tag) in brown.tagged_words(tagset='universal') if tag == 'VERB'])
Verbs2 = set(
    [word for (word, tag) in Carroll
     if tag == 'VB' and len(word) > 3]
)

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

def spawn_users(num):
    users = []
    for i in range(num):
        name = "user_%d" % i
        gstring = s1str.getGString()
        producer = Producer(name, gstring)
        gNums = [random.randint(0,10) for i in range(5)]
        bNums = [random.randint(0,10) for i in range(5)]
        wordTypes = [Adjectives2, Pronouns, Nouns2, IntransitiveVerbs, Verbs2]
        gWords = []
        bWords = []
        for i, wtype in enumerate(wordTypes):
            gWords += sample(wtype, gNums[i])
            bWords += sample(wtype, bNums[i])
        wr = WordRule(gWords, bWords)
        ar = ApostropheRule(random.random(), random.random(), random.random())
        lr = LengthRule(random.random()*-1, random.random(), random.random())
        aEvaluator = evaluator.Evaluator([wr, ar, lr])
        users.append(environment.User(name, producer, True, aEvaluator, True))
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


