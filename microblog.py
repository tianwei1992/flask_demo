from app import app, db, cli    # 这里app是app.__init__
from app.models import User, Post    # 这里app是app目录


@app.shell_context_processor   # 无需导入就可在flask db中使用以下实例
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
