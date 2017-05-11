from producer_class import Producer
import evaluator
from length import LengthRule
from apostrophe import ApostropheRule
from closeword import WordRule
import sqlite3

""" A user is an object containing information about a user and functions to control 
    the production and evaluation of text, and the mutation of the user.
    Attributes:
        environment:    The environment object that a specific user is associated with
        producer:       The producer object that produces text for a specific user
        evaluator:      The evaluator object that evaluates text for a user
        potBuds:        The potetional "buddies" that a user has
        name:           The name of the user
        dbID:           The id of the user in the environment database
        iterations:     A list of lists of posts, each corresponding to an iteration of 
                        the environment
        iteration_size: the number of post to be generated by each grammar of the 
                        producer each iteration
        isProducer:     A boolean representing whether or not this user is a text 
                        producing user in the environment
        isConsumer:     A boolean representing whether or not this user plays an 
                        evaluating roll in the environment
    """
class User:
    def __init__(self, name, producer, isProducer, evaluator, isEvaluator, iteration_size=10):
        self.environment = None
        self.producer = producer
        self.evaluator = evaluator
        self.potBuds = {}
        self.name = name
        self.dbID = None
        self.iterations = []
        self.iteration_size=iteration_size
        self.isProducer = isProducer
        self.isConsumer = isEvaluator

    """Returns posts generated by the user for a given iteration"""
    def get_iteration(self, iteration_index):
        return self.producer.get_iteration(iteration_index, self.iteration_size)

    """evaluates a set of posts, and mutates the evaluation rules"""
    def evaluate_iteration(self, posts):
        for post in posts:
            result = self.evaluator.evaluate(post)
            oUser = post.author
            if result > 0:
                post.upvotes += 1
            if result < 0:
                post.downvotes += 1
            post.score += result

    """mutates the producer"""
    def mutate(self):
        self.producer.mutate()

""" Environment is an object that organizes and controls the actions of a group of
    agents
    Attributes:
        db:         the name of the file corresponding to the SQLite database
        users:      the users in the environment (generated by a function passed to the
                    environment)
        producers:  the users in the environment that serve a text producing role
        consumers:  the users in teh environment that serve a text evaluating role
        iteration:  the current iteration the environment has run through
        iterations: a record of the posts posted each iteration.  CURRENTLY UNUSED
        userDict:   a dictionary mapping each user to their name.  for buddy purposes
    """
class Environment:
    def __init__(self, spawn, db_name):
        self.db = db_name
        self.users = spawn()
        self.producers = self.get_producers()
        self.consumers = self.get_consumers()
        self.iteration = 0
        self.iterations = []
        self.userDict = {user.name: user for user in self.users}
        for user in self.users:
            user.environment = self

    """Returns the user object for a given username"""
    def lookupUser(self, uname):
        return self.userDict[uname]
    
    """Creates the SQLite database and tables for the environment"""
    def setup_db(self):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute('''CREATE TABLE users 
                            (user_id INTEGER PRIMARY KEY, name TEXT)''')
        c.execute('''CREATE TABLE posts
                            (post_id INTEGER PRIMARY KEY, poster_id INTEGER, 
                             poster TEXT, time TEXT, post TEXT, score INTEGER,
                             upvotes INTEGER, downvotes INTEGER, iteration INTEGER)''')
        conn.commit()
        conn.close()

    """Adds the environment's users to the user table of the SQLite database"""
    def add_users_to_db(self):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        for user in self.users:
            c.execute('INSERT INTO users(name) VALUES (?)', (user.name, ))
            c.execute('SELECT user_id FROM users WHERE name = ?', (user.name, ))
            uid = c.fetchone()[0]
            user.dbID = uid
            if user.isProducer:
                user.producer.userID = uid
        conn.commit()
        conn.close()

    """Returns the users in the system that serve a text producing role"""
    def get_producers(self):
        return [user for user in self.users if user.isProducer]
    
    """Returns the consumers in the system that serve a text evaluating role"""
    def get_consumers(self):
        return [user for user in self.users if user.isConsumer]

    """Runs the environment through an iteration of text production, text evaluation,
       and mutation"""
    def run_iteration(self):
        posts = []
        for user in self.producers:
            posts += user.get_iteration(self.iteration)
        for user in self.consumers:
            user.evaluate_iteration(posts)
        for user in self.producers:
            user.mutate()
        self.iteration += 1
        return posts
        
    """Adds each post from a list of posts to the database"""
    def insert_posts(self, posts):
        pvals = [(p.authorID, p.author.name, str(p.timestamp), p.text,  p.score, p.upvotes, p.downvotes, p.iteration_index) for p in posts]
        conn = sqlite3.connect(self.db)
        c=conn.cursor()
        c.executemany('''INSERT INTO posts(poster_id, poster, time, post, score, upvotes, 
                         downvotes, iteration) VALUES (?,?,?,?,?,?,?,?)''', pvals)
        conn.commit()
        conn.close()
   
   """Returns the database ID corresponding to a user with a given username"""
    def get_id_for_user(self, username):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        uname = (username,)
        result = c.execute('SELECT user_id from users where name = ?', uname)
        conn.commit()
        conn.close()
        return result[0][0]

