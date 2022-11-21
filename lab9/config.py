import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # General config
    DEBUG = False
    DEVELOPMENT = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ENCRYPTED_KEY'
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(object):
    # General config
    DEBUG = True
    DEVELOPMENT = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ENCRYPTED_KEY'
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'dev': DevConfig,
    'default': Config,
}
