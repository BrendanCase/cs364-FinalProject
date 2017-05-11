import metric
from nltk.corpus import wordnet as wn
import random

CHANCE = .2
""" WordRule
    A WordRule is an evaluation metric whihc compares words in a post against
    words in a list.  More specifically, it compares each word in a sentance against
    a list of good words and a list of bad words.  The more similar a word is to a
    good word, the higher the score, and conversely for a list of bad words.

    A WordRule is an instance of the Metric class and so implements the evaluate and
    mutate fucntions.


"""
class WordRule(metric.Metric):
    
    def __init__(self, goodWords, badWords):
        self.goodWords = set(goodWords)
        self.badWords = set(badWords)

    def getLCHDepth(self, syns1, syns2):
        """ gets the depth of the lowest common hypernym of two elements
            in a synset"""
        lch = syns1.lowest_common_hypernyms(syns2)
        if len(lch) == 0:
            return 0
        minDepth = wn.synset(lch[0].name()).min_depth()
        return minDepth

    def getSimilarity(self, word1, word2):
        """ For two words, finds the two closest definitions and return the depth"""
        w1syns = wn.synsets(word1)
        w2syns = wn.synsets(word2)
        if 0 in (len(w1syns), len(w2syns)):
            return 0
        depths = [self.getLCHDepth(w1syn, w2syn) for w1syn in w1syns for w2syn in w2syns]
        return max(depths)
        
    def getRating(self, word, wordList):
        """ finds the similiraty score of a given word and its most similar word in 
            a word list"""
        if len(wordList) == 0:
            return 0
        else:
            return max([self.getSimilarity(word, oWord) for oWord in wordList])

    def getSentanceScore(self, sentance, wordList):
        """ creates a score for a sentance by comparing the similarity of each word in
            the sentance to each word in the word list"""
        sentanceWords = sentance.split(' ')
        return sum([self.getRating(word, wordList) for word in sentanceWords])

    def evaluate(self, post):
        string = post.text
        """ scores the sentance agaisnt the good and bad word lists"""
        return self.getSentanceScore(string, self.goodWords) - self.getSentanceScore(string, self.badWords)

    def mutate(self, post, value):
        """ if the sentance was upvoted, remove a word from it from goodWords or put it in badWords.  If it was downvoted, remove a word from it from badwords, or add it to goodWords """
        string = post.text
        words = string.split(' ')
        if random.random() < .5:
            return
        if value > 0:
            cand = [w for w in words if w not in self.goodWords]
            if len(cand) > 0:
                word = random.choice([w for w in words if w not in self.goodWords])
                self.goodWords.add(word)
                if word in self.badWords and len(self.badWords) > 1:
                    self.badWords.remove(word)
        elif value < 0:
            cand = [w for w in words if w not in self.badWords]
            if len(cand) > 0:
                word = random.choice(cand)
                self.badWords.add(word)
                if word in self.goodWords and len(self.goodWords) > 1:
                    self.goodWords.remove(word)
