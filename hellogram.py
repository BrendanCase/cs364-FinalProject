import nltk
from nltk.corpus import brown
from nltk.corpus import gutenberg
from random import sample

from producer.producer_class import Producer

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


def main():
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

    gram = test.induceGrammar()
    cp = nltk.ChartParser(gram)
    for i in range(10):
        (prods, post) = test.getPost(gram)
        print(post)
        print()


#program entry point
if __name__ == '__main__':
    main()