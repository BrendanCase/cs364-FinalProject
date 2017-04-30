import random as rand
import metric

class LengthRule(metric.Metric):
    def __init__(self, second, first, zero):
        self.second = second
        self.first = first
        self.zero = zero
    
    def evaluate(self, string):
        return (.001) * self.second * (len(string) ** 2) + self.first * len(string) + self.zero
    
    def mutate(self, bull, change):
        if rand.Random > .5:
            self.second = self.second - change
            if self.second == 0:
                self.second = -1
        if rand.Random >.5:
            self.first = self.first - change
        if rand.Random > .5:
            self.zero = self.zero - change
