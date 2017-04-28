import nltk

class WordRule(metric.Metric):
    def __init__(self, goodWords, badWords):
        self.goodWords = goodWords
        self.badWords = badWords

    def getLCHDepth(self, syns1, syns2):
        lch = csyn.lowest_common_hypernyms(syns2)
        minDepth = wn.synset(lch[0].name()).min_depth()

    def getSimilarity(self, word1, word2):
        w1syns = wn.synsets(word1)
        w2syns = wn.synsets(word2)
        depths = [self.getLCHDepth(w1syn, w2syn) for w1syn in w1syns for w2syn in w2syns])
        return max(depths)
        
    def getRating(self, word, wordList):
        return max([self.getSimilarity(word, oWord) for oWord in wordList])

    def getSentanceScore(self, sentance, wordList):
        sentanceWords = sentance.split(' ')
        return sum([self.getRating(word, wordList) for word in sentanceWords])

    def evaluate(self, string):
        return self.getSentanceScore(string, self.goodWords) - self.getSentanceScore(string, self.badWords)

    def mutate(self, string, value):
        words = string.split(' ')
        if value < 0:
            self.badWords = self.badWords | set(words)
        elif value > 0:
            self.goodWords = self.goodWords | set(words)

