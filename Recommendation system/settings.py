class Config(object):
    DEBUG = False
    MONGO_URI = URL
    SECRET_KEY = Your secret key
    MONGODB_SETTINGS = {
        "db": "Recommendation_system",
        "host": MONGO_URI,
    }
