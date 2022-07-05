
class config:
    SQLALCHEMY_DATABASE_URI="sqlite:///app.db"
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # secret key for test created by secret lib ib python
    SECRET_KEY='900fb6004e1d7a5a54750cba5b91d2b6'
    SESSION_TYPE='filesystem'
    SESSION_PERMANENT = False

class Development(config):
    DEBUG=True


class Production(config):
    DEBUG=False