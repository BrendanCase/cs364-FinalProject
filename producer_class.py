import nltk
import random
import re
import numpy as np
import datetime

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

""" A post is a post object, containing information about a given textpost.
    Attributes:
        text:      A string contiang the text of the post
        timestamp: A datetime object containg the time the post was generated
        score:     The score of a given post
        upvotes:   The number upvotes the post has recieved
        downvotes: The number of downvotes a post has recieved
        author:    The bot who generated it
        generation:     The round or generation the post was made in.
    """
class Post:
    def __init__(self, string, author, authorID, iteration_index=None):
        self.text = string
        self.author = author
        self.authorID = authorID
        self.iteration_index = iteration_index
        self.timestamp = datetime.datetime.today()
        self.score = 0
        self.upvotes = 0
        self.downvotes = 0


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
    return grammarString.replace(old_rule, new_rule)

def makerhs(t, p): #return a rhs form of production string: " t [p] | "
    return '\"' + t + '\"' + ' [' + str(p) + '] | '


class Grammar:
    
    def __init__(self, grammar):
        self.grammar = grammar
        self.posts = []

    def mutate(self):
        #temporary mutation function
        start = self.grammar._start
        leftHandSides = [prod._lhs for prod in self.grammar._productions]
        leftHandSide = random.choice(leftHandSides)
        productions = self.grammar.productions(lhs=leftHandSide)
        otherProductions = [prod for prod in self.grammar.productions() if prod not in productions]
        newProbs = np.random.dirichlet(np.ones(len(productions)),size=1)[0]
        for i, newProb in enumerate(newProbs):
            prod = productions[i]
            lhs = prod._lhs
            rhs = prod._rhs
            newProd = nltk.ProbabilisticProduction(lhs,rhs,prob=newProb)
            otherProductions.append(newProd)
        newGrammar = nltk.PCFG(start, otherProductions)
        return Grammar(newGrammar)

    """ getPost
    takes a nltk.PCFG grammar
    creates a string by traversing the grammar's parse tree by selecting a child based on its probability
    and adding terminals (leaves) to the string
    traverses the trees with a pre-order style
    returns the string
    """
    def get_post(self):
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
    
    def make_post(self, user, uid, iteration):
        text = self.get_post()
        newPost =  Post(text, user, uid, iteration)
        self.posts.append(newPost)
        return newPost

    def get_score(self):
        return sum([post.score for post in self.posts])

class Producer:

    def __init__(self, user, gram):
        self.user = user
        self.userID = None
        if isinstance(gram, str):
            self.parent_grammar = Grammar(self.induce_grammar(gram))
        else: #gram is a PCFG already
            self.parent_grammar = gram
        self.child_grammars = self.get_children()
        self.grammars = self.get_grammars()

    """ inducegrammar
    return a probabilistic context-free grammar from the grammar string
    handles errors making the grammar to be handled cleanly in the future
    (for now return a default pcfg)
    """
    def induce_grammar(self, gramString):
        try:
            ret = nltk.grammar.PCFG.fromstring(gramString)
        except ValueError as e:
            print("There was something wrong with %s's grammar:" %self.user)
            print(e)
            ret = nltk.data.load('default_grammar.pcfg')
        return ret

    def get_children(self, generation_size=2):
        children = []
        for i in range(generation_size):
            children.append(self.parent_grammar.mutate())
        return children

    def get_grammars(self):
        return [self.parent_grammar] + self.child_grammars

    def get_iteration(self, iteration_index, iteration_size):
        current_iteration = []
        for grammar in self.grammars:
            for i in range(iteration_size):
                current_iteration.append(grammar.make_post(self.user, self.userID, iteration_index))
        return current_iteration

    def mutate(self):
        best_grammar = max(self.grammars, key=lambda x: x.get_score())
        self.parent_grammar = best_grammar
        self.child_grammars = self.get_children()
        self.grammars = self.get_grammars()




