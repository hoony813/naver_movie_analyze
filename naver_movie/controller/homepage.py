from flask import Flask, render_template, request,jsonify
import json

from naver_movie.naver_movie_blueprint import naver_movie_blueprint


@naver_movie_blueprint.route('/')
def homepage():
    with open('./naver_movie/static/movie_score_main_2.json', encoding='UTF8') as json_file:
        data = json.load(json_file)

    return render_template('homepage.html',json_data = data)

