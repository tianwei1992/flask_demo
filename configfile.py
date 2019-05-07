import os

class Config(object):
    """父类是普通的object"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
