import os

class Config:
    BASEDIR=os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = "dev-secret-key"
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(BASEDIR,"placement_portal.db")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    
    REDIS_URL= "redis://localhost:6379/0"
    
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300
    
    
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "namankhurana2017@gmail.com"
    MAIL_PASSWORD = "iyatfbrqsplcfbdt"
    MAIL_DEFAULT_SENDER = MAIL_USERNAME