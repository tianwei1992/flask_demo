import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from configfile import Config    # 从同级的config.py文件导入...


app = Flask(__name__)
app.config.from_object(Config)  # 从configfile.py文件的Config类导入配置，解耦.其中app.config是Flask类的一个特性而不是configfile.py的文件名

db = SQLAlchemy(app)   # 注册插件Flask-SQLAlchemy
migrate = Migrate(app, db)    # 注册插件  Flask-Migrate

login = LoginManager(app)
login.login_view = 'login'    # 用户未登入的情况下试图访问一个 login_required 视图，Flask-Login 会 闪现一条消息并把他们重定向到c此

# 生产模式下，报警邮件配置
# 测试方法：
# 1. 在本地模拟的邮件服务器
# python -m smtpd -n -c DebuggingServer localhost:8025
# 然后另一个终端produce模式启动flask，然后制造错误，就会发送邮件
# export MAIL_SERVER=localhost
# export MAIL_PORT=8025
# export FLASK_DEBUG=0
#
# export FLASK_APP=microblog.py &&  FLASK_ENV=produce flask run --host='0.0.0.0' --port='10024'
# 2. 配置好真实地址，发到真正的邮件服务器 
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        
        # 设置告警级别，只有严重到ERROR才发邮件
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

from app import routes, models, errors    # 不引入models.py等于没有这个文件，然后db migrate不生效


# 日志配置
if not app.debug:
    # ...

    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')    # 服务器每次启动先出一行日志
