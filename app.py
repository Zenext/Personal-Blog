from flask import Flask, render_template, redirect, url_for, request, session, g

from models import User, Post
from postForm import *

from datetime import date

app = Flask(__name__)
    
app.secret_key = '[;fsdfeeff,?RTewr34355511@@234##@!Jnsruuqqqqqq'
    
def get_categories():
    categories = []
    category = Post.select()
    for cat in category:
        if cat.category not in categories:
            categories.append(cat.category)

    return categories

def get_posts():
    return Post.select().order_by(Post.date.desc())

def get_archive():
    months = [x.date.strftime('%B %Y') for x in Post.select()]
    return list(set(months))

@app.route('/')
@app.route('/page/<page_number>')
def main(*args, **kwargs):
    title = 'Home'
    addpost = False
    if 'username' in session:
        title = 'Admin home'
        addpost = True
    return render_template('main.html', addpost=addpost, posts=get_posts(),
            recent_posts=get_posts(),
            categories=get_categories(),
            archives=get_archive())

@app.route('/about')
def about():
    return render_template('about.html',
                           title='About me')

# route for handling the login
# TODO: use decorator
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        admin = User.get(User.name == 'admin')
        if request.form['username'] != admin.name  or request.form['password'] != admin.password:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username'] = request.form['username']
            g.user = 'admin'
            return redirect(url_for('main'))
    return render_template('login.html', error=error)

# route for viewing posts
@app.route('/post/<postname>')
def post(postname):
    post = Post.get(Post.header == postname)
    return render_template('post.html', post=post,
            posts=get_posts(),
            categories=get_categories(),
            recent_posts=get_posts(),
            archives=get_archive())


# route for adding new posts, only if logged as admin
@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
    form = addPostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post.create(header=form.name.data,
                    text=form.text.data,
                    date=date.today(),
                    category=form.category.data)
    
    return render_template('addpost.html', form=form, 
            posts=get_posts(),
            recent_posts=get_posts(),
            archives=get_archive())

@app.route('/contact')
def contact():
    return render_template('contact.html', posts=get_posts(),
            recent_posts=get_posts(),
            categories=get_categories(),
            archives=get_archive())

@app.route('/archives')
def archives():
    months = [x.date for x in Post.select()]
    unique_months = list(set(months))
    return render_template('archives.html', posts=get_posts(),
            recent_posts=get_posts(),
            categories=get_categories(),
            months=unique_months,
            archives=get_archive())

@app.route('/archives/<month>')
def posts_by_month(month):
    return render_template('main.html',
            posts=Post.select().where(Post.date.year == 2015),
            recent_posts=get_posts(),
            categories=get_categories(),
            archives=get_archive())

@app.route('/category/<category_name>')
def category(category_name):
    return render_template('main.html',
            posts=Post.select().where(Post.category == category_name).order_by(Post.date.desc()),
            recent_posts=get_posts(),
            categories=get_categories(),
            archives=get_archive())

app.run(debug=True)