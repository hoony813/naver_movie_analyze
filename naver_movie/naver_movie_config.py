import os

class NaverMovieConfig(object):
    TESTING = True

    DEBUG = True

    USER_RELOADER = True

    SECRET_KEY = os.urandom(24)

    LOG_FILE_PATH = 'resource/log/naver_movie_flask.log'

    MONGO_URI = "mongodb://localhost:27017/naver_movie"

