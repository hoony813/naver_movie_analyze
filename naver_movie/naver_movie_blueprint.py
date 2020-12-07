from flask import Blueprint

naver_movie_blueprint = Blueprint('naver_movie',__name__,template_folder='./templates',static_folder='./static')