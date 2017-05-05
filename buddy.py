import metric

class BuddyRule(metric.Metric):
    def __init__(self, value):
        self.value = value
    
    def evaluate(self, string):
        return self.value
        
    def mutate(self, bull, change):
        if change > 1:
            self.value -= 2
        self.value += 1