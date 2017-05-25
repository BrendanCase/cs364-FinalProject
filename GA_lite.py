from producer_class import Producer
from evaluator_class import Evaluator
from user_class import User
import s1str
import s2str
import s3str
import s4str

Iterations = 100
PopulationSize = 20
PostsPerGrammar = 3
ChildrenPerGrammar = 2
ExtraEvaluators = False
Users = []

"""
PROGRAM ENTRY POINT
"""
def main():
    global Users
    # get user input
    Users = spawn_users()
    for i in range(Iterations):
        create_generation()
        posts = get_posts(i)
        evaluate_posts(posts)
        compete_for_survival()
        print_results(posts)

def spawn_users():
    users = []
    prod_types = [s1str.getGString(), s2str.getGString(), s3str.getGString(), s4str.getGString()]
    for i in range(PopulationSize):
        user = User("user_%d" % i,
                    None,
                    Evaluator())
        user.producer = Producer(user, prod_types[i%4][0], prod_types[i%4][1])
        users.append(user)
    for i in range(PopulationSize):
        users.append(User("eva_%d" % i,
                          None,
                          Evaluator()))
    return users

def create_generation():
    for u in Users:
        if u.producer is not None:
            u.producer.create_generation(ChildrenPerGrammar)

def get_posts(iter):
    posts = []
    for u in Users:
        if u.producer is not None:
            posts.extend(u.get_iteration(iter))
    return posts

def evaluate_posts(posts):
    for user in Users:
        user.evaluate_iteration(posts)

def compete_for_survival():
    for u in Users:
        if u.producer is not None:
            u.producer.compete()

def print_results(posts):
    # pvals = [(p.authorID, p.author.name, str(p.timestamp), p.text, p.score, p.upvotes, p.downvotes, p.iteration_index)
    #          for p in posts]
    for p in posts:
        print(p.author.name, end=' : ')
        print(p.upvotes, end=", ")
        print(p.downvotes)
        print(p.text)
        print('-----')


if __name__ == '__main__':
    main()