import os

projectRoot = os.path.abspath(os.path.dirname('..'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'replace-me-in-production'
    TEMPLATES_AUTO_RELOAD = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + f'{projectRoot}\\data\\sqlite\\database.sqlite'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
