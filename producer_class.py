import nltk
import random
import math
import re
import datetime
from collections import defaultdict
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
    probs = [1/len(termlist)] * len(termlist)
    probs[0] += 1 - math.fsum(probs)
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
        self.mCount = 0 # how many merges this Grammar currently has

    def mutate(self):
        self.mutate_weights() #MUTATE TYPE 1
        new_prods = []
        for user in self.user.buddies:
            bud_prod = user.producer
            if random.random() <= 0.05: # there's a %5 chance of grabbing a bud's terminal
                bw = self._getbudword(bud_prod)
                if bw is not None:
                    new_prods.append(bw)
        if random.random() <= 0.1: # %10 chance to grab some random new noun or adjective
            nw = self._getnewword()
            if nw is not None:
                new_prods.append(nw)
        if len(new_prods) > 0:
            self.add_new(new_prods) # MUTATE TYPE 2
        if random.random() <= 0.01: # %1 chance to breed with a bud grammar
            bud = random.choice(self.user.buddies)
            sep = self._getsep()
            self.merge(sep, bud.producer) # MUTATE TYPE 3
        if random.random() <= 0.02: # %2 change to break up from a breeding
            self.separate() # MUTATE TYPE 4
        return Grammar(self.grammar, self.user)
        
    def add_new(self, prods):
        gram = self.grammar
        old_prods = gram.productions()
        prob_map = defaultdict(list)
        for prod in prods:
            prob_map[prod.lhs()].append(prod.prob())
        for op in old_prods:
            fix = math.fsum(prob_map[op.lhs()]) / len(gram.productions(op.lhs()))
            prods.append(nltk.ProbabilisticProduction(op.lhs(), op.rhs(), prob=op.prob() - fix))
        try:
            self.grammar = nltk.PCFG(gram.start(), self._balance(prods))
        except ValueError:
            print('ERROR2')
            pass
        
    def mutate_weights(self):
        gram = self.grammar
        new_prods = []
        for lhs in set([p.lhs() for p in gram.productions()]):
            if random.random() <= 0.1: #this prod group gettin' mutated
                prod_group = gram.productions(lhs) #must change the weights of the productions which share prod's lhs
                if len(prod_group) == 1:
                    new_prods.extend(gram.productions(lhs))
                    continue
                change = random.gauss(0, .05)
                fix = change / (len(prod_group) - 1)
                change_p = random.choice(prod_group)
                for p in prod_group:
                    if p == change_p and (p.prob() + change) > 0:
                        new_prods.append(nltk.ProbabilisticProduction(p.lhs(), p.rhs(), prob=(p.prob() + change)))
                    elif (p.prob() - fix) > 0:
                        new_prods.append(nltk.ProbabilisticProduction(p.lhs(), p.rhs(), prob=(p.prob() - fix)))
            else:
                new_prods.extend(gram.productions(lhs))
        try:
            self.grammar = nltk.PCFG(gram.start(), self._balance(new_prods))
        except ValueError: #there's still just that chance things won't quite add up
            print('ERROR1')
            pass

    """ merge
    takes a punctuation, conjunction and second grammar to act as the second
    dependent/independent clause or phrase and modifies the current grammar to include this
    more complex compound sentence
    Currently enforces no sort of subject agreement between the two terminal sets
    Returns a tuple of the new start state and new productions
    """
    def merge(self, conjunction, budProd):
        grammar2 = budProd.parent_grammar.grammar
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
        # then do it for orig nonterminals for later separation
        for p in self.grammar.productions():
            lhs = nltk.Nonterminal(str(p.lhs()) + '1')
            rhs = []
            for sym in p.rhs():
                if isinstance(sym, nltk.Nonterminal):
                    rhs.append(nltk.Nonterminal(str(sym) + '1'))
                else:
                    rhs.append(sym)
            new_prods.append(nltk.ProbabilisticProduction(lhs, rhs, prob=p.prob()))
        # now make the head to combine the two production trees
        CC = nltk.Nonterminal(conjunction)
        new_prods.append(nltk.ProbabilisticProduction(CC, [conjunction], prob=1.0))
        P1 = nltk.Nonterminal(str(self.grammar.start()) + '1')
        P2 = nltk.Nonterminal(str(grammar2.start()) + '2')
        S = nltk.Nonterminal('S')
        head = nltk.ProbabilisticProduction(S, [P1, CC, P2], prob=1.0)
        new_prods.append(head)
        try:
            self.grammar = nltk.PCFG(S, new_prods)
            # self.user.producer.wordlist = {**self.user.producer.wordlist, **budProd.wordlist}
            self.mCount += 1
        except ValueError as E:
            print('ERROR3')
            pass

    def separate(self):
        gram = self.grammar
        if self.mCount > 0:
            start = None
            subprods = []
            if random.random() <= 0.5:
                start = gram.productions(gram.start())[0].rhs()[0]
                subprods = [p for p in gram.productions() if str(p.lhs())[-1] == str(1)]
            else:
                start = gram.productions(gram.start())[0].rhs()[2]
                subprods = [p for p in gram.productions() if str(p.lhs())[-1] == str(2)]
            try:
                self.grammar = nltk.PCFG(start, subprods)
                self.mCount -= 1
            except ValueError as E:
                print(E)
                print('ERROR4')
                pass

    def _getsep(self):
        pure_conj = ['and', 'but', 'for', 'so', 'yet']
        sub_conj = ['after', 'although', 'because', 'even though', 'since', 'whereas', 'though', 'unless', 'which', 'whereas']
        conj_adv = ['nevertheless', 'furthermore', 'however', 'in fact', 'hence', 'likewise', 'besides', 'consequently',
                    'for example', 'indeed', 'still', 'that is']
        t1 = random.sample([', ' + pc for pc in pure_conj], 2)
        t2 = random.sample(sub_conj, 2)
        t3 = random.sample(['; ' + ca + ',' for ca in conj_adv], 2)
        t4 = '; '
        return random.choice([random.choice(t1), random.choice(t2), random.choice(t3), t4])

    """ balance
    takes a list of probabilities
    """
    def _balance(self, prods):
        prod_groups = defaultdict(list)
        new_prods = []
        for p in prods:
            prod_groups[p.lhs()].append(p.prob())
        for lhs in prod_groups.keys():
            if math.fsum(prod_groups[lhs]) != 1: #need to fix one of these boys then
                fix_p = random.choice([p for p in prods if p.lhs() is lhs])
                # print(math.fsum(prod_groups[lhs]))
                # print('balancing ', fix_p)
                new_p = nltk.ProbabilisticProduction(lhs, fix_p.rhs(), prob=(fix_p.prob() + (1-math.fsum(prod_groups[lhs]))))
                # print('and made ', new_p)
                new_prods.append(new_p)
                prods = [p for p in prods if p is not fix_p]
        return prods + new_prods

    """ getnewword
    picks a new noun or adjective from the word bank and makes a new
    production for the grammar. should be called only once per mutation for best results on
    the probabilities
    returns the new production
    """
    def _getnewword(self):
        if random.random() <= 0.5:
            word = random.choice(list(set([word for (word, tag) in WordBank if tag == 'NN' and len(word) > 3])))
            word_type = 'SingNoun'
        else:
            word = random.choice(list(set([word for (word, tag) in WordBank if tag == 'JJ' and len(word) > 3])))
            word_type = 'Adj'
        r = re.compile(r'%s[12]*' %word_type)
        lhs = [p.lhs() for p in self.grammar.productions() if r.search(str(p.lhs()))]
        if word in self.user.producer.wordlist[word_type]:
            return None
        self.user.producer.wordlist[word_type].append(word) #remember to update the word list!
        return nltk.ProbabilisticProduction(lhs[0], [word], prob=1/len(lhs))

    def _getbudword(self, budProd):
        done = False
        word_type = None
        while not done:  # make sure you have a place to add this terminal
            word_type = random.choice(list(budProd.wordlist.keys()))
            if word_type in self.user.producer.wordlist.keys():
                done = True
        word = random.choice(budProd.wordlist[word_type])
        r = re.compile(r'%s[12]*' % word_type)
        lhs = [p.lhs() for p in self.grammar.productions() if r.search(str(p.lhs()))]
        if word in self.user.producer.wordlist[word_type]:
            return None
        self.user.producer.wordlist[word_type].append(word)
        return nltk.ProbabilisticProduction(lhs[0], [word], prob=1/len(lhs))

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
        newPost =  Post(text, user.name, uid, iteration)
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
        self.child_grammars = []
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




