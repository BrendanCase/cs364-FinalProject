import nltk

class LengthRule(metric.Metric):
    def __init__(self, second, first, zero):
        self.second = second
        self.first = first
        self.zero = zero
    
    def eval(self, string):
        return self.second * (len(string) ** 2) + self.first * len(string) + self.zero
    
    def mutate(self, bull, change):
        if rand.Random > .5:
            self.second = self.second - change
            if self.second == 0:
                self.second = -1
        if rand.Random >.5:
            self.first = self.first - change
        if rand.Random > .5:
            self.zero = self.zero - change