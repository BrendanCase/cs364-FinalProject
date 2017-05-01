from flask import Flask, url_for, render_template
import sqlite3
#import environment
app = Flask(__name__)

#currentEnvironment = environment.Environment()

def get_post(database, post_id):
    db = '%s.db' % database
    conn = sqlite3.connect(db)
    c=conn.cursor()
    c.execute('SELECT post_id, poster, post, time, score, upvotes, downvotes, iteration FROM posts where post_id = ?', (post_id, ))
    post = c.fetchone()
    print(post)
    conn.close()
    return post
    #return (27, "aUser", "the quick brown fox jumped over the lazy dog", 
    #        "OCT-17-17 2:28:01", 7, 9, 2, 8)

def get_posts(database):
    db = '%s.db' % database
    conn = sqlite3.connect(db)
    c=conn.cursor()
    c.execute('SELECT post_id, poster, post, time, score, upvotes, downvotes, iteration FROM posts')
    posts = c.fetchall()
    conn.close()
    return [{'post_id': p[0], 'poster': p[1], 'text': p[2], 'time': p[3], 'score': p[4],
     'upvotes': p[5], 'downvotes': p[6], 'iteration': p[7]} for p in posts]
    posts

@app.route('/')
def index():
    return 'Index Page'

@app.route('/<database>/posts/')
def show_posts(database):
    posts = get_posts(database)
    style_url = url_for('static', filename='style.css')
    return render_template('posts.html', stylesheet=style_url, posts=posts)

@app.route('/<database>/post/<int:post_id>')
def show_post(database, post_id):
    post = get_post(database, post_id)
    style_url = url_for('static', filename='style.css')
    return render_template('post.html', stylesheet=style_url, id=post[0], 
                           poster=post[1], text=post[2], time=post[3], score=post[4], 
                           upvotes=post[5], downvotes=post[6], iteration=post[7])
