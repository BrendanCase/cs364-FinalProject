"""
ApostopheRule
gives a small score change to evaluation score for each apostrophe in the post
"""

import random as rand
import metric
import math

class ApostropheRule(metric.Metric):
    def __init__(self):
        self.score_bump = 5

    def evaluate(self, post):
        string = post.text
        return string.count('\'') * self.score_bump
    
    def mutate(self, bull, change):
        pass
