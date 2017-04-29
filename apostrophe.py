import nltk

class ApostropheRule(metric.Metric):
    def __init__(self, second, first, zero):
        self.second = second
        self.first = first
        self.zero = zero
    
    def eval(self, string):
        total = string.count('\'')
        max = max([word.count('\'') for word in string])
        average = total/len([word in string])
        return self.second * exp(max) + self.first * log(total*average) + self.zero
    
    def mutate(self, bull, change):
        if rand.Random > .5:
            self.second = self.second - change
        if rand.Random >.5:
            self.first = self.first - change
        if rand.Random > .5:
            self.zero = self.zero - change