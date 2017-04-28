import nltk
import random
import re

""" producer class
A producer is...

******
Public Methods:

induceGrammar
getPost
addTerminals
******

Authors:
Brendan Case
Joe Martin
Jackson Martin
"""
class Producer:

    def __init__(self, user, gramString):
        self.user = user
        self.grammar_string = gramString #the skeleton grammar string for this producer to start with

    """ induceGrammar
    return a Probabilistic Context-Free Grammar from the grammar string
    handles errors making the grammar to be handled cleanly in the future
    (for now return a default PCFG)
    """
    def induceGrammar(self):
        try:
            ret = nltk.grammar.PCFG.fromstring(self.grammar_string)
        except ValueError as e:
            print("There was something wrong with %s's grammar:" %self.user)
            print(e)
            self.grammar_string = ''.join(open('default_grammar.pcfg'))
            ret = nltk.grammar.PCFG.fromstring(self.grammar_string)
        return ret

    """ getPost
    takes a nltk.PCFG grammar
    creates a string by traversing the grammar's parse tree by selecting a child based on its probability
    and adding terminals (leaves) to the string
    traverses the trees with a pre-order style
    returns the string
    """
    def getPost(self, grammar):
        Q = [grammar.start()]
        tok = []
        while len(Q) > 0:
            lhs = Q.pop(0)
            prods = grammar.productions(lhs)  # get the productions with this lhs NT
            prod = self._pickprod(prods)
            for sym in list(reversed(prod.rhs())):  # so we need to add all the rules to parse
                if isinstance(sym, nltk.Nonterminal):  # if symbol is a nonterminal, add it
                    Q.insert(0, sym)
                else:
                    tok.append(str(sym))
        return ' '.join(tok)

    """ addTerminals
    takes a nonterminal object and list of strings
    builds a new set of rules for the producer's grammar string from these strings
    with uniform probability transitions
    """
    def addTerminals(self, termType, termList):
        probs = [1/len(termList) for i in termList]
        probs[0] += 1 - sum(probs)
        rule_str = termType + ' -> '
        for prob, terminal in zip(probs, termList):
            rule_str += self._makerhs(terminal, prob)
        new_rule = rule_str[:-2] #get rid of last " |"
        old_rule = termType+ ' -> \'*\' [1.0]'
        self.grammar_string = self.grammar_string.replace(old_rule, new_rule)
        #return nothing, the grammar string rep has been updated!

    ######################################################
    #                    PRIVATE                         #
    ######################################################


    def _pickprod(self, P): #takes list of productions P and selects a production based on its probability
        r = random.random()
        sum = 0
        for prod in P:  # we need to choose a production
            sum += prod.prob()
            if sum >= r:
                return prod
                # here we denote prod's probability with P(prod), so then using elementary identities of probability:
                # prod selected <=> sum(P(p') for p' in P up to prod) >= r
                #               <=> 1 >= sum(P(p') before prod) + P(prod) >= r
                #               <=> 1 - sum(P(p') up to prod) >= r - sum(P(p') before prod) - P(prod)
                #               <=> sum(P(p') after prod) >= r > sum(P(p') before prod), since no p' before prod was picked
                #               <=> r in range(0, P(prod)) (inclusive)
                # But then P(r in range(0, P(prod)) = P(prod) since r is uniform in [0,1]



    def _makerhs(self, T, P): #return a rhs form of production string: " T [P] | "
        return '\"' + T + '\"' + ' [' + str(P) + '] | '