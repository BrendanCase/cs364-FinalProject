import random as rand
import metric

class LengthRule(metric.Metric):
    def __init__(self):
        self.score_bump = 1
    
    def evaluate(self, string):
        c = 1
        if len(string) in range(25, 100):
            c = 2
        elif len(string) in range(10, 200):
            c = 1
        else:
            c = -5
        return self.score_bump * c
        
    def mutate(self, bull, change):
        # if rand.random() > .5:
        #     self.second = self.second - change
        #     if self.second == 0:
        #         self.second = -1
        # if rand.random() >.5:
        #     self.first = self.first - change
        # if rand.random() > .5:
        #     self.zero = self.zero - change
        pass
