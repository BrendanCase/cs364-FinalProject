import nltk
import random

class Producer:

    def __init__(self, user, gramString):
        self.user = user
        self.grammar = nltk.grammar.PCFG.fromstring(gramString)
        #TODO: decide on necessary subsets of terminal sets (e.g. Nouns, Verbs, etc.)

    def getPost(self):
        Q = [self.grammar.start()]
        tok = []
        while len(Q) > 0:
            lhs = Q.pop(0)
            prods = self.grammar.productions(lhs)  # get the productions with this lhs NT
            prod = self.pickProd(prods)
            for sym in list(reversed(prod.rhs())):  # so we need to add all the rules to parse
                if isinstance(sym, nltk.Nonterminal):  # if symbol is a nonterminal, add it
                    Q.insert(0, sym)
                else:
                    tok.append(str(sym))
        return ' '.join(tok)

    ######################################################
    #                    HELPERS                         #
    ######################################################


    def pickProd(self, P):
        r = random.random()
        sum = 0
        for prod in P:  # we need to choose a production
            sum += prod.prob()
            if sum >= r:  # this is the branch we have decided to descend
                return prod