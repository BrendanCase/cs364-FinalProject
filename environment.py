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
    def __init__(self, string, author, genearation=None):
        self.text = string
        self.author = author
        self.generation = generation
        self.timestamp = datetime.datetime.today()
        self.score = 0
        self.upvotes = 0
        self.downvotes = 0


class User():
    def __init__(self, name, generation_size=10):
        self.producer = Producer()
        self.evaluator = Evaluator()
        self.name = name
        self.generations = []
        self.generation_size=10
        
    def make_post(self, generation):
        text = self.producer.get_post(self.producer.grammar)
        return Post(text, self.name, generation)

    def get_generation(self, generation):
        current_generation = []
        for i in range(self.generation_size):
            current_generation.append(self.make_post(generation))
        self.generations.append(current_generation)
        return current_generation

    def evaluate_post(self, post):
        self.evaluator.evaluate(post.text)

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

    def run_generation():
        posts = []
        for user in self.produers:
            posts += user.get_generation(self.generation)
        for user in self.consumers():
            user.evaluate_generation()
        generation += 1
        
