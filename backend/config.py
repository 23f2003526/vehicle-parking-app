# app.config['SECRET_KEY'] = 'your_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Config():
    DEBUG = False
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///Database.db"
    DEBUG = True
    # SECURITY_PASSWORD_HASH = 'bcrypt'
    # SECURITY_PASSWORD_SALT = 'thisshouldbekeptsecret'
    SECRET_KEY = "your_secret_key"
 
    WTF_CSRF_ENABLED = False

    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 30
    CACHE_REDIS_PORT = 6379

    EXPORT_FOLDER = "./exports"
