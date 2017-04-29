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

""" addterminals
takes a nonterminal object and list of strings
builds a new set of rules for the producer's grammar string from these strings
with uniform probability transitions
"""
def addterminals(grammarString, termtype, termlist):
    probs = [1/len(termlist) for i in termlist]
    probs[0] += 1 - sum(probs)
    rule_str = termtype + ' -> '
    for prob, terminal in zip(probs, termlist):
        rule_str += makerhs(terminal, prob)
    new_rule = rule_str[:-2] #get rid of last " |"
    old_rule = termtype+ ' -> \'*\' [1.0]'
    grammarString = grammarString.replace(old_rule, new_rule)
    #return nothing, the grammar string rep has been updated!

def makerhs(t, p): #return a rhs form of production string: " t [p] | "
    return '\"' + t + '\"' + ' [' + str(p) + '] | '


class Grammar:
    
    def __init__(self, grammar):
        self.grammar = grammar
        self.posts = []

    def mutate(self):
        #return new grammar object

""" getPost
    takes a nltk.PCFG grammar
    creates a string by traversing the grammar's parse tree by selecting a child based on its probability
    and adding terminals (leaves) to the string
    traverses the trees with a pre-order style
    returns the string
    """
    def getPost(self):
        Q = [self.grammar.start()]
        tok = []
        while len(Q) > 0:
            lhs = Q.pop(0)
            prods = self.grammar.productions(lhs)  # get the productions with this lhs NT
            prod = self._pickprod(prods)
            for sym in list(reversed(prod.rhs())):  # so we need to add all the rules to parse
                if isinstance(sym, nltk.Nonterminal):  # if symbol is a nonterminal, add it
                    Q.insert(0, sym)
                else:
                    tok.append(str(sym))
        return ' '.join(tok)

    def _pickprod(self, p): #takes list of productions p and selects a production based on its probability
        r = random.random()
        sum = 0
        for prod in p:  # we need to choose a production
            sum += prod.prob()
            if sum >= r:
                return prod
                # here we denote prod's probability with p(prod), so then using elementary identities of probability:
                # prod selected <=> sum(p(p') for p' in p up to prod) >= r
                #               <=> 1 >= sum(p(p') before prod) + p(prod) >= r
                #               <=> 1 - sum(p(p') up to prod) >= r - sum(p(p') before prod) - p(prod)
                #               <=> sum(p(p') after prod) >= r > sum(p(p') before prod), since no p' before prod was picked
                #               <=> r in range(0, p(prod)) (inclusive)
                # but then p(r in range(0, p(prod)) = p(prod) since r is uniform in [0,1]
    
    def make_post(self, name, iteration):
        text = self.get_post()
        newPost =  Post(text, name, iteration)
        self.posts = newPost
        return newPost

    def get_score(self):
        return sum([post.score for post in self.posts])

class Producer:

    def __init__(self, user, gramstring):
        self.user = user
        self.grammar_string = gramstring #the skeleton grammar string for this producer to start with
        self.parent_grammar = Grammar(self.induce_grammar())
        self.child_grammars = self.get_children()
        self.grammars = self.get_grammars()

    """ inducegrammar
    return a probabilistic context-free grammar from the grammar string
    handles errors making the grammar to be handled cleanly in the future
    (for now return a default pcfg)
    """
    def inducegrammar(self):
        try:
            ret = nltk.grammar.pcfg.fromstring(self.grammar_string)
        except ValueError as e:
            print("There was something wrong with %s's grammar:" %self.user)
            print(e)
            self.grammar_string = ''.join(open('default_grammar.pcfg'))
            ret = nltk.grammar.PCFG.fromstring(self.grammar_string)
        return ret

    def get_children(self, generation_size=2):
        children = []
        for i in range(generation_size):
            children.append(self.parent_grammar.mutate())
        self.child_grammars = children

    def get_grammars(self):
        return [self.parent_grammar] + self.child_grammars

    def get_iteration(self, iteration_index, iteration_size):
        current_iteration = []
        for grammar in self.grammars:
            for i in range(iteration_size):
                current_iteration.append(grammar.make_post(self.user, iteration_index))
        return current_iteration

    def mutate(self):
        best_grammar = max(self.grammars, lambda x: x.get_score())
        self.parent_grammar = best_grammar
        self.child_grammars = self.get_children
        self.grammars = self.get_grammars




