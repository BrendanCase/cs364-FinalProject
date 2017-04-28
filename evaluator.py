import nltk

class Evaluator():
    def __init__(self, metric):
        self.metric = metric #metric is the list of functions which the Evaluator evaluates the strings on
        self.minusThresh = -10
        self.plusThresh = 15
    
    def evaluate(str):
        v = 0 #v is the value gained by the Evaluator by reading this meme
        for m in self.metric: #m is one of the members of metric
            v += m.eval(str)
        if v < minusThresh:
            return -1
        if v > plusThresh:
            return 1
        return 0
        
    def mutate(