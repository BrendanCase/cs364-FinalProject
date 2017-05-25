import metric
from collections import defaultdict

class BuddyRule:
    def __init__(self, user):
        self.score_bump = 1.5
        self.bud_dict = defaultdict(int)

    
    def evaluate(self, post):
        if post.author in self.user.producer.buddies:
            return self.score_bump * self.bud_dict[post.author]
        return -1
        
    def mutate(self, post, value):
        pass