import metric
from collections import defaultdict

class BuddyRule(metric.Metric):
    def __init__(self, user):
        self.score_bump = 1.5
        self.user = user
        self.bud_dict = defaultdict(int)
    
    def evaluate(self, post):
        if post.author in self.user.producer.buddies:
            return self.score_bump * self.bud_dict[post.author]
        return -1
        
    def mutate(self, post, value):
        if value > 0:
            self.bud_dict[post.author] += 1
            self.bud_dict[post.author] = min(self.bud_dict[post.author], 10)
            if self.bud_dict[post.author] >= 3:
                self.user.producer.buddies.append(post.author)
        if value < 0:
            self.bud_dict[post.author] -= 1
            self.bud_dict[post.author] = max(self.bud_dict[post.author], 0)
            if self.bud_dict[post.author] < 3:
                self.user.producer.buddies = [u for u in self.user.producer.buddies if u is not post.author]