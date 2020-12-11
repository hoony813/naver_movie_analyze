from flask import request, render_template

from naver_movie.naver_movie_blueprint import naver_movie_blueprint
from naver_movie.model.get_movies_score import get_movies_score

@naver_movie_blueprint.route('/compare_graph', methods=['GET', 'POST'])
def compare_graph():
    _id = request.args.get('id')
    print(_id)
    data = get_movies_score(_id)
    print(data)
    return render_template('movie_score.html',json_data = data)
