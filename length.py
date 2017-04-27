import nltk

class LengthRule(metric.Metric):
    def __init__(self, second, first, zero):
        self.second = second
        self.first = first
        self.zero = zero
    
    def eval(self, string):
        return self.second * (len(string) ** 2) + self.first * len(string) + self.zero
    
    def mutate(self,
