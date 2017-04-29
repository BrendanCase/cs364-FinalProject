import Producer from producer_class

""" A post is a post object, containing information about a given textpost.
    Attributes:
        text:      A string contiang the text of the post
        timestamp: A datetime object containg the time the post was generated
        score:     The score of a given post
        upvotes:   The number upvotes the post has recieved
        downvotes: The number of downvotes a post has recieved
        author:    The bot who generated it
        generation:     The round or generation the post was made in.
    """
class Post():
    def __init__(self, string, author, iteration_index=None):
        self.text = string
        self.author = author
        self.iteration_index = iteration_index
        self.timestamp = datetime.datetime.today()
        self.score = 0
        self.upvotes = 0
        self.downvotes = 0

class User():
    def __init__(self, name, grammar generation_size=10):
        self.producer = Producer()
        self.evaluator = Evaluator()
        self.name = name
        self.parent_grammar = grammar
        self.child_grammars = self.get_children(grammar) 
        self.generations = []
        self.generation_size=generation_size

    def get_iteration(self, iteration_index):
        return self.producer.get_iteration(iteration_index)

    def evaluate_iteration(self, iteration):
        for post in iteration:
            self.evaluator.evaluate(post.text)

    def mutate():
        self.producer.mutate()

class Environment():
    def __init__(self):
        self.users = spawn_users()
        self.producers = self.get_producers()
        self.consumers = self.get_consumers()
        self.generation = 0
        self.generations = []

    def get_producers(self):
        return [user for user in self.users if user.producer]
    
    def get_consumers(self):
        return [user for user in self.users if user.consumer]

    def run_iteration():
        posts = []
        for user in self.produers:
            posts += user.get_iteration(self.iteration)
        for user in self.consumers():
            user.evaluate_iteration(posts)
        for user in self.producers:
            user.mutate()
        iteration += 1
        
