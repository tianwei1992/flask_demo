from flask import render_template, flash, redirect

from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user, posts=posts)    # 注意模板路径没有包含templates目录


@app.route('/login', methods=['GET', 'POST'])
def login():
    """只有post且验证成功才是rediret首页，不成功的post和get都是redirect到login页"""
    form = LoginForm()
    if form.validate_on_submit():    # if request_method == 'POST'..
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data)) # generate flashed_messages
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)
