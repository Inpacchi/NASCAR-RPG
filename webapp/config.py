import os

projectRoot = os.path.abspath(os.path.dirname('..'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'replace-me-in-production'
    TEMPLATES_AUTO_RELOAD = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + f'{projectRoot}\\data\\sqlite\\database.sqlite'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['internal@endlessgalaxy.dev']

    # FOR TESTING PURPOSES ONLY
    # MAIL_SERVER = 'localhost'
    # MAIL_PORT = 8025

    # GOOGLE SETTINGS
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True