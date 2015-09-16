from flask import Flask, render_template, redirect, url_for, request, session

from models import User, Post
from postForm import *

import time
from datetime import date

app = Flask(__name__)

app.secret_key = '[;fsdfeeff,?RTewr34355511@@234##@!Jnsruuqqqqqq'

@app.route('/')
def main():
    title = 'Home'
    addpost = False
    if 'username' in session:
        title = 'Admin home'
        addpost = True
    return render_template('main.html', addpost=addpost, posts=Post.select())

@app.route('/about')
def about():
    return render_template('about.html',
                           title='About me')


# route for handling the login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        admin = User.get(User.name == 'admin')
        if request.form['username'] != admin.name  or request.form['password'] != admin.password:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username'] = request.form['username']
            return redirect(url_for('main'))
    return render_template('login.html', error=error)

# route for viewing posts
@app.route('/post/<postname>')
def post(postname):
    post = Post.get(Post.header == postname)
    return render_template('post.html', header=post.header, text=post.text, date=post.created_date)

# route for adding new posts, only if logged as admin
@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
    form = addPostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post.create(header=form.name.data,
                    text=form.text.data,
                    created_date=date.today().strftime('%B %d, %Y'))
    
    if 'username' in session:
        return render_template('addpost.html', form=form)
    else:
        return redirect(url_for('login'))
        
        
app.run(debug=True)