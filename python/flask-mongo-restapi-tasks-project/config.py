class Config:
    SECRET_KEY = "0863d8af18948ebbc784189207978566"
    MONGO_URI = "mongodb://localhost:27017/tasksDB"

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False

