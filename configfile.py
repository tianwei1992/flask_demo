import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))    # 从.env文件导入环境变量

class Config(object):
    """父类是普通的object"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # ???

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    BAIDU_TRANSLATOR_APPID = os.environ.get('BAIDU_TRANSLATOR_APPID')
    BAIDU_TRANSLATOR_SECRETKEY = os.environ.get('BAIDU_TRANSLATOR_SECRETKEY')

    # 日志输出到stdout，heroku logs查看
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    ADMINS = ['tianweigrace@gmail.com']

    # 分页
    POSTS_PER_PAGE = 4

    # 语言的国际化
    LANGUAGES = ['en', 'es', 'zh_Hans_CN', 'zh']
