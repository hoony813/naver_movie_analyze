from flask import request, render_template

from naver_movie.naver_movie_blueprint import naver_movie_blueprint

@naver_movie_blueprint.route('/compare_graph?id=<path:id>')
def compare_graph(id):
    temp = id
    temp1 = 'movie_score_' + temp + '.json'
    return render_template('movie_score.html',num=temp, json=temp1)
