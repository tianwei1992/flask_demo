from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from configfile import Config    # 从同级的config.py文件导入...


app = Flask(__name__)
app.config.from_object(Config)  # 从configfile.py文件的Config类导入配置，解耦.其中app.config是Flask类的一个特性而不是configfile.py的文件名

db = SQLAlchemy(app)   # 注册插件Flask-SQLAlchemy
migrate = Migrate(app, db)    # 注册插件  Flask-Migrate


from app import routes, models    # 不引入models.py等于没有这个文件，然后db migrate不生效
