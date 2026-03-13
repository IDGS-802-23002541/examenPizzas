
class Config(object):
    SECRET_KEY='Clave nueva'
    SESSION_COOKIE_SECURE=False

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:0510@127.0.0.1/pizzeria'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
