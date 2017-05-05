import nltk

class Evaluator():
    def __init__(self, metric):
        self.metric = metric #metric is the list of functions which the Evaluator evaluates the strings on
        self.minusThresh = -10
        self.plusThresh = 15
    
    def evaluate(self, str):
        v = 0 #v is the value gained by the Evaluator by reading this meme
        for m in self.metric: #m is one of the members of metric
            b = m.evaluate(str)
            if b is not None:
                v += b
        if v < self.minusThresh:
            self.mutate(str, -1)
            return -1
        if v > self.plusThresh:
            self.mutate(str, 1)
            return 1
        return 0
        
    def mutate(self, string, vote):
        for met in self.metric:
            met.mutate(string, vote)
