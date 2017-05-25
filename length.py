import random as rand
import metric

class LengthRule(metric.Metric):
    def __init__(self):
        self.score_bump = 5

    def evaluate(self, post):
        string = post.text
        c = 1
        if len(string) in range(50, 100):
            c = len(string) / 15
        elif len(string) in range(20, 200):
            c = len(string) / 30
        else:
            c = -len(string) / 10
        return self.score_bump * c
        
    def mutate(self, bull, change):
        # if rand.random() > .95:
        #     self.second = self.second - change
        #     if self.second == 0:
        #         self.second = 1
        # if rand.random() >.95:
        #     self.first = self.first - change
        #     if self.first == self.zero:
        #         self.first += 1
        # if rand.random() > .95:
        #     self.zero = self.zero - change
        #     if self.zero == self.first:
        #         self.zero -= 1
        pass
