import nltk
import random
from nltk.parse.generate import generate
from ProducerClass import Producer

"""
features we may need...
-
"""

TerminalList = ['the', 'all', 'and', 'cats', 'dogs', 'rats', 'jump', 'or']

def pcfg_generate(PCFG):
    D = {}
    for prod in PCFG.productions():
        D[prod] = prod.prob()
    Q = [PCFG.start()]
    sen = []
    while len(Q) > 0:
        lhs = Q.pop(0)
        prods = PCFG.productions(lhs) #get the productions with this lhs NT
        prod = pickProd(prods, D)
        for sym in list(reversed(prod.rhs())):  # so we need to add all the rules to parse
            if TerminalList.count(str(sym)) == 0:  # if symbol is a nonterminal, add it
                Q.insert(0, sym)
            else:
                sen.append(str(sym))
    return sen


def pickProd(productions, D):
    r = random.random()
    sum = 0
    for prod in productions:  # we need to choose a production
        sum += D[prod]
        if sum >= r:  # this is the branch we have decided to descend
            return prod


def main():
    testPG = nltk.grammar.PCFG.fromstring("""
    S -> NP VP [1.0]
    NP -> P N [.7] | NP C NP [.3]
    VP -> V [1.0]
    P -> 'the' [.7] | 'all' [.3]
    N -> 'cats' [.4] | 'dogs' [.4] | 'rats' [.2]
    V -> 'jump' [1.0]
    C -> 'and' [.5] | 'or' [.5]""")

    test = Producer('/u/_junebug_', """
        S -> NP VP [1.0]
        NP -> P N [.7] | NP C NP [.3]
        VP -> V [1.0]
        P -> 'the' [.7] | 'all' [.3]
        N -> 'cats' [.4] | 'dogs' [.4] | 'rats' [.2]
        V -> 'jump' [1.0]
        C -> 'and' [.5] | 'or' [.5]""")

    for i in range(10):
        print(test.getPost())
    print("-----------------")
    for i in range(10):
        print(' '.join(pcfg_generate(testPG)))

#program entry point
if __name__ == '__main__':
    main()