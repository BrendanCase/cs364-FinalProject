import nltk

class WordRule(metric.Metric):
    def __init__(self, goodWords, badWords):
        self.goodWords = goodWords
        self.badWords = badWords

    def getLCHDepth(syns1, syns2):
        lch = csyn.lowest_common_hypernyms(syns2)
        minDepth = wn.synset(lch[0].name()).min_depth()

    def getSimilarity(self, word1, word2):
        w1syns = wn.synsets(word1)
        w2syns = wn.synsets(word2)
        depths = [getLCHDepth(w1syn, w2syn) for w1syn in w1syns for w2syn in w2syns])
        return max(depths)
        
    def getRating(word, wordList):
        return max([getSimilarity(word, oWord) for oWord in wordList])

    def getSentanceScore(sentance, wordList):
        sentanceWords = sentance.split(' ')
        return sum([getRating(word, wordList) for word in sentanceWords])

    def evaluate(string):
        return getSentanceScore(string, self.goodWords) - getSentanceScore(string, self.badWords)
