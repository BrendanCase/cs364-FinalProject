import nltk

class Evaluator:
    def __init__(self, metrics, user):
        self.metrics = metrics #metric is the list of functions which the Evaluator evaluates the strings on
        self.minusThresh = -10
        self.plusThresh = 25
        self.user = user
    
    def evaluate(self, post):
        v = 0 #v is the value gained by the Evaluator by reading this meme
        print(post.text)
        for m in self.metrics: #m is one of the members of metric
            b = m.evaluate(post)
            print(m, b, end=' ')
            v += b
            print()
        print('%d -> ' %v, end='')
        if v < self.minusThresh:
            print('downvote')
            self.mutate(post, -1)
            return -1
        if v > self.plusThresh:
            self.mutate(post, 1)
            print('upvote')
            return 1
        print('nothing')
        return 0
        
    def mutate(self, post, vote):
        for met in self.metrics:
            met.mutate(post, vote)
