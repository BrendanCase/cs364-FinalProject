import random as rand
import metric
import math

class ApostropheRule(metric.Metric):
    def __init__(self, second, first, zero):
        self.second = second
        self.first = first
        self.zero = zero
    
    def evaluate(self, string):
        total = string.count('\'')
        aMax = max([word.count('\'') for word in string])
        average = total/len([word for word in string])
        return self.second * math.exp(aMax) + self.first * math.log((total*average) + 1) + self.zero
    
    def mutate(self, bull, change):
        if rand.Random > .5:
            self.second = self.second - change
        if rand.Random >.5:
            self.first = self.first - change
        if rand.Random > .5:
            self.zero = self.zero - change
