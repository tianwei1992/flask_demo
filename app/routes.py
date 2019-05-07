from flask import render_template
from app import app

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

