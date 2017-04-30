import nltk
import random
import numpy as np
import scipy

def mutateWeights(grammar):
    start = grammar._start
    leftHandSides = [prod._lhs for prod in grammar._productions]
    leftHandSide = random.choice(leftHandSides)
    productions = grammar.productions(lhs=leftHandSide)
    otherProductions = [prod for prod in grammar.productions() if prod not in productions]    
    lower = 0
    upper = 1
    standarddeviationsayswhat = .2
    p1 = random.choice(productions)
    p1.prob = scipy.stats.truncnorm.rvs((lower - p1.prob)/standarddeviationsayswhat, (upper - p1.prob)/standarddeviationsayswhat, loc=p1.prob, scale = standarddeviationsayswhat)
    sum = sum([p.prob for p in productions])
    for p in productions:
        p.prob = p.prob/sum 
    otherProductions.append(productions)
    newGrammar = nltk.PCFG(start, otherProductions)
    return newGrammar