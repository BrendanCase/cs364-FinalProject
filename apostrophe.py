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
    
    def mutate(self,