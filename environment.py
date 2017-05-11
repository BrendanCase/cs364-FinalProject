from producer_class import Producer
import evaluator
from length import LengthRule
from apostrophe import ApostropheRule
from closeword import WordRule
import sqlite3

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

    def get_iteration(self, iteration_index):
        return self.producer.get_iteration(iteration_index, self.iteration_size)

    def evaluate_iteration(self, posts):
        for post in posts:
            result = self.evaluator.evaluate(post)
            oUser = post.author
            if result > 0:
                post.upvotes += 1
            if result < 0:
                post.downvotes += 1
            post.score += result

    def mutate(self):
        self.producer.mutate()

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

    def lookupUser(self, uname):
        return self.userDict[uname]
    
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

    def get_producers(self):
        return [user for user in self.users if user.isProducer]
    
    def get_consumers(self):
        return [user for user in self.users if user.isConsumer]

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
        

    def insert_posts(self, posts):
        pvals = [(p.authorID, p.author.name, str(p.timestamp), p.text,  p.score, p.upvotes, p.downvotes, p.iteration_index) for p in posts]
        conn = sqlite3.connect(self.db)
        c=conn.cursor()
        c.executemany('''INSERT INTO posts(poster_id, poster, time, post, score, upvotes, 
                         downvotes, iteration) VALUES (?,?,?,?,?,?,?,?)''', pvals)
        conn.commit()
        conn.close()
    
    def get_id_for_user(self, username):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        uname = (username,)
        result = c.execute('SELECT user_id from users where name = ?', uname)
        conn.commit()
        conn.close()
        return result[0][0]

