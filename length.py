import random as rand
import metric

class LengthRule(metric.Metric):
    def __init__(self, second, first, zero):
        self.second = second
        if self.second <= 0:
            self.second = 1
        self.first = first
        self.zero = zero
        if self.zero == self.first:
            self.zero -= 1
    
    def evaluate(self, string):
        return 4 * self.second * (len(string) - self.first) * (len(string) - self.zero) / ((self.first - self.zero) (self.zero - self.first))
        
    def mutate(self, bull, change):
        if rand.random() > .95:
            self.second = self.second - change
            if self.second == 0:
                self.second = 1
        if rand.random() >.95:
            self.first = self.first - change
            if self.first == self.zero:
                self.first += 1
        if rand.random() > .95:
            self.zero = self.zero - change
            if self.zero == self.first:
                self.zero -= 1