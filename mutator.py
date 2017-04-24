import nltk
import random
import numpy as np

def mutateWeights(grammar):
    start = grammar._start
    leftHandSides = [prod._lhs for prod in grammar._productions]
    leftHandSide = random.choice(leftHandSides)
    productions = grammar.productions(lhs=leftHandSide)
    otherProductions = [prod for prod in grammar.productions() if prod not in productions]
    newProbs = np.random.dirichlet(np.ones(len(productions)),size=1)[0]
    for i, newProb in enumerate(newProbs):
        prod = productions[i]
        lhs = prod._lhs
        rhs = prod._rhs
        newProd = nltk.ProbabilisticProduction(lhs,rhs,prob=newProb)
        otherProductions.append(newProd)
    newGrammar = nltk.PCFG(start, otherProductions)
    return newGrammar


    
