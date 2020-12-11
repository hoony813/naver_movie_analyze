import os
from flask import Flask, request, url_for
from flask_pymongo import PyMongo


client = PyMongo()

def create_app():
    app = Flask(__name__)
    ## 플라스크 앱 설정
    from naver_movie.naver_movie_config import NaverMovieConfig
    app.config.from_object(NaverMovieConfig)
    app.config.suppress_callback_exceptions = True
    app.env = 'development'

    ## 로그 초기화
    from naver_movie.naver_movie_logger import Log
    log_filepath = os.path.join(app.root_path,
                                 app.config['LOG_FILE_PATH'])
    Log.init(log_filepath=log_filepath)
    
    ### 블루프린트 설정
    from naver_movie.controller import compare_graph, homepage, naver_movie_info, two_movie_infos

    from naver_movie.naver_movie_blueprint import naver_movie_blueprint
    app.register_blueprint(naver_movie_blueprint)

    ### 데이터베이스 설정
    client.init_app(app)

    return app