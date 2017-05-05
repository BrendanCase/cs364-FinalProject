import nltk
import random
import math
import numpy as np
import datetime
from nltk.corpus import gutenberg

""" producer class

Authors:
Brendan Case
Joe Martin
Jackson Martin
"""

WordBank = nltk.pos_tag(gutenberg.words('whitman-leaves.txt'))

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
    
    def __init__(self, grammar, user):
        self.user = user #the user which owns this grammar
        self.grammar = grammar
        self.posts = []

    def mutate(self):
        self.mutate_weights() #MUTATE TYPE 1

        new_prods = []
        for user in self.user.buddies:
            bud_prod = user.producer
            if random.random() <= 0.05: # there's a %5 chance of grabbing a bud's terminal
                done = False
                word_type = None
                while not done: # make sure you have a place to add this terminal
                    word_type = random.choice(bud_prod.wordlist.keys())
                    if word_type in self.user.producer.wordlist.keys():
                        done = True
                word = random.choice(bud_prod.wordlist[word_type])
                lhs = [p.lhs() for p in self.grammar.productions() if str(p.lhs()) in word_type][0]
                new_prods.append(nltk.ProbabilisticProduction(lhs, [word], prob=1/len(self.user.producer.wordlist[word_type])))
        if random.random() <= 0.05: # %5 chance to grab some random new noun or adjective
            if random.random() <= 0.5:
                word = random.choice(set([word for (word, tag) in WordBank if tag == 'NN' and len(word) > 3]))
                word_type = 'SingNoun'
            else:
                word = random.choice(set([word for (word, tag) in WordBank if tag == 'JJ' and len(word) > 3]))
                word_type = 'Adj'
            lhs = [p.lhs() for p in self.grammar.productions() if str(p.lhs()) in word_type][0]
            new_prods.append(nltk.ProbabilisticProduction(lhs, [word], prob=1/len(self.user.producer.wordlist[word_type])))
        if len(new_prods) > 0:
            self.add_new(new_prods) # MUTATE TYPE 2

        if random.random() <= 0.01: # %1 chance to breed with a bud grammar
            bud = random.choice(self.user.buddies)
            sep = self._getsep()
            self.merge(sep, bud) # MUTATE TYPE 3

        return Grammar(self.grammar, self.user)
        
    def add_new(self, prods):
        gram = self.grammar
        new_prods = []
        for prod in prods: # these are the productions we are adding
            effected_prods = gram.productions(prod.lhs())
            new_prods.extend([p for p in gram.productions() if p not in effected_prods])
            fix = prod.prob()/len(effected_prods)
            new_prods.append(prod)
            for p in effected_prods:
                new_prods.append(nltk.ProbabilisticProduction(p.lhs(), p.rhs(), prob=p.prob() - fix))
        self.grammar = nltk.PCFG(gram.start(), new_prods)
        
    def mutate_weights(self):
        gram = self.grammar
        new_prods = gram.productions()
        for prod in gram.productions():
            if random.random() <= 0.1: #this prod gettin' mutated
                prods = gram.productions(prod.lhs()) #must change the weights of the productions which share prod's lhs
                if len(prods) == 1:
                    continue
                new_prods = [p for p in new_prods if p not in prods] # temporarily remove the prods we are changing
                change = random.gauss(0, .01/(math.sqrt(2)/math.pi))
                fix = change/(len(prods) - 1)
                for p in prods:
                    if p == prod:
                        new_prods.append(nltk.ProbabilisticProduction(p.lhs(), p.rhs(), prob=(p.prob() + change)))
                    else:
                        new_prods.append(nltk.ProbabilisticProduction(p.lhs(), p.rhs(), prob=(p.prob() - fix)))
        self.grammar = nltk.PCFG(gram.start(), new_prods)

    """ merge
    takes a punctuation, conjunction and second grammar to act as the second
    dependent/independent clause or phrase and modifies the current grammar to include this
    more complex compound sentence
    Currently enforces no sort of subject agreement between the two terminal sets
    Returns a tuple of the new start state and new productions
    """
    def merge(self, conjunction, grammar2):
        #first go through each of the nonterminals in grammar2 and make sure they do not overlap
        new_prods = []
        for p in grammar2.productions():
            lhs = nltk.Nonterminal(str(p.lhs()) + '2')
            rhs = []
            for sym in p.rhs():
                if isinstance(sym, nltk.Nonterminal):
                    rhs.append(nltk.Nonterminal(str(sym) + '2'))
                else:
                    rhs.append(sym)
            new_prods.append(nltk.ProbabilisticProduction(lhs, rhs, prob=p.prob()))
        # then change the start rule of this grammar
        start_prods = self.grammar.productions(self.grammar.start())
        new_starts = [nltk.ProbabilisticProduction(nltk.Nonterminal(str(p.lhs()) + '1'),
                                                   [nltk.Nonterminal(str(sym)) for sym in p.rhs()],
                                                   prob=p.prob())
                      for p in start_prods]
        new_prods += (new_starts + [p for p in self.grammar.productions() if p not in start_prods])
        # now make the head to combine the two production trees
        CC = nltk.Nonterminal(conjunction)
        new_prods.append(nltk.ProbabilisticProduction(CC, [conjunction], prob=1.0))
        P1 = nltk.Nonterminal(str(self.grammar.start()) + '1')
        P2 = nltk.Nonterminal(str(grammar2.start()) + '2')
        S = nltk.Nonterminal('S')
        head = nltk.ProbabilisticProduction(S, [P1, CC, P2], prob=1.0)
        new_prods.append(head)
        return S, new_prods

    def _getsep(self):
        pure_conj = ['and', 'but', 'for', 'so', 'yet']
        sub_conj = ['after', 'although', 'because', 'even though', 'since', 'whereas', 'though', 'unless', 'which', 'whereas']
        conj_adv = ['nevertheless', 'furthermore', 'however', 'in fact', 'hence', 'likewise', 'besides', 'consequently',
                    'for example', 'indeed', 'still', 'that is']
        t1 = random.sample([', ' + pc for pc in pure_conj], 2)
        t2 = random.sample(sub_conj, 2)
        t3 = random.sample(['; ' + ca + ', ' for ca in conj_adv], 2)
        t4 = '; '
        return random.choice([t1, t2, t3, t4])

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

    def __init__(self, user, gram, wordlist):
        self.user = user
        self.userID = None
        if isinstance(gram, str):
            self.parent_grammar = Grammar(self.induce_grammar(gram), user)
        else: #gram is a PCFG already
            self.parent_grammar = gram
        self.child_grammars = self.get_children()
        self.grammars = self.get_grammars()
        self.wordlist = wordlist

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




