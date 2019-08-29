from app.models import User, Post    # 这里app是app目录
from app import create_app, db, cli


app = create_app()
cli.register(app)


@app.shell_context_processor   # 无需导入就可在flask db中使用以下实例
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
