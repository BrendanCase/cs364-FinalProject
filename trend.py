import metric

class TrendRule(metric.Metric):
    def __init__(self):
        self.score_bump = 5

    def evaluate(self, post):
        if 2 * post.upvotes >= post.downvotes >= 1:
            return 2 * self.score_bump
        elif 2 * post.downvotes >= post.upvotes >= 1:
            return -self.score_bump
        return 1

    def mutate(self, bull, change):
        pass