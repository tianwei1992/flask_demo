import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask, request, current_app

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l


from configfile import Config    # 从同级的config.py文件导入...


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('请先登录.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp, url_prefix='/')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    if not app.debug and not app.testing:
        # 邮件配置
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # 日志配置
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


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


from app import models    # 不引入models.py等于没有这个文件，然后db migrate不生效


# 语言国际化配置
# 每个请求都会调用这个函数，从request对象的accetpt_languages匹配到服务器最适合的语言
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


