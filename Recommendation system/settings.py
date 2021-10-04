class Config(object):
    DEBUG = False
    MONGO_URI = "mongodb://localhost:27017/Recomendation_system?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
    SECRET_KEY = 'ea5c5bf03a1a40938e4eadae8b304bc5'
    MONGODB_SETTINGS = {
        "db": "Recommendation_system",
        "host": MONGO_URI,
    }