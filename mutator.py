import nltk
import random
import numpy as np
import scipy

def mutateWeights(grammar):
    start = grammar._start
    leftHandSides = [prod._lhs for prod in grammar._productions]o
    leftHandSide = random.choice(leftHandSides)
    oldProductions = grammar.productions(lhs=leftHandSide)
    otherProductions = [prod for prod in grammar.productions() if prod not in productions] 
    productions = []
    p1 = random.choice(productions)
    oldProductions.remove(p1)
    lower = 0
    upper = 1
    standarddeviationsayswhat = .2
    newProb = scipy.stats.truncnorm.rvs((lower - p1.prob)/standarddeviationsayswhat, (upper - p1.prob)/standarddeviationsayswhat, loc=p1.prob, scale = standarddeviationsayswhat)
    sum = sum([p.prob for p in oldProductions]) + newProb
    productions.append(p1._lhs,p1._rhs, newProb/sum)
    for p in oldProductions:
        lhs = p._lhs
        rhs = p._rhs
        pro = p.prob()
        newProd = nltk.ProbabilisticProduction(lhs,rhs,prob=pro/sum)    
        productions.append(newProd)
    otherProductions.append(productions)
    newGrammar = nltk.PCFG(start, otherProductions)
    return newGrammar