class BaseConfig(object):
    ADMINS = []
    DEBUG = True
    TESTING = False
    VERBOSE = False
    PROPAGATE_EXCEPTIONS = True

    MONGO_URI = "mongodb://localhost:27017/playmate"

    SENTRY_DSN = ""
    SENTRY_RELEASE = "0.1"
    APP_SECRET = "mallsini"
    EXPIRED_DAYS = 360

    GOOGLE_ID = "cloud.google.com/console and get your ID"
    GOOGLE_SECRET = "cloud.google.com/console and get the secret"

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'JPG', 'PNG', 'JPEG'])
    FCM_API_KEY = "AAAAWrTMXdA:APA91bHpWyxNxXEM3EdhqbWp92UU3qLvoAXUORjZZxaPYGXVOs2L0IDwxo2mj9uAs9C60LwvwKSaF-PUDTqJ9-AjUmeylYt0DcfefALdRVk9WFF1LI5cTslEQqQ0n0p55PQ1MD-KOcG2"


class DevelopmentConfig(BaseConfig):
    SENTRY_DSN = "https://4488ccd131374904958b2188aaa2c7e5:6bf733cb60c4431fb18751f17a4f63e8@sentry.io/154960"
    MONGO_URI = "mongodb://localhost:27017/playmate"


class TestingConfig(BaseConfig):
    pass


class StagingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    "development": "playmate.config.DevelopmentConfig",
    "testing": "playmate.config.TestingConfig",
    "staging": "playmate.config.StagingConfig",
    "production": "playmate.config.ProductionConfig"
}
