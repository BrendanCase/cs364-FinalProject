"""
ApostopheRule
gives a small score change to evaluation score for each apostrophe in the post
"""

import random as rand
import metric
import math

class ApostropheRule(metric.Metric):
    def __init__(self):
        self.score_bump = 1

    def evaluate(self, post):
        return post.count('\'') * self.score_bump
    
    def mutate(self, bull, change):
        pass
