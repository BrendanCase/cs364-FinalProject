from nltk.corpus import brown
from random import sample

from producer.producer_class import Producer

Adjectives = set([word for (word, tag) in brown.tagged_words(tagset='universal') if tag == 'ADJ'])
Pronouns = set([word for (word, tag) in brown.tagged_words(tagset='universal') if tag == 'PRON'])
Determiners = set([word for (word, tag) in brown.tagged_words(tagset='universal') if tag == 'DET'])
Nouns = set([word for (word, tag) in brown.tagged_words(tagset='universal') if tag == 'NOUN'])
IntransitiveVerbs = set([w.strip('\n') for w in open('intransitives.txt')])
Verbs = set([word for (word, tag) in brown.tagged_words(tagset='universal') if tag == 'VERB'])

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
    test.addTerminals('Adj', sample(Adjectives, 15))
    test.addTerminals('Pronoun', sample(Pronouns, 8))
    test.addTerminals('Det', sample(Determiners, 6))
    test.addTerminals('Noun', sample(Nouns, 20))
    test.addTerminals('IV', sample(IntransitiveVerbs, 10))
    test.addTerminals('TV', sample(Verbs, 20))

    gram = test.induceGrammar()
    for i in range(10):
        print(test.getPost(gram))
        print()


#program entry point
if __name__ == '__main__':
    main()