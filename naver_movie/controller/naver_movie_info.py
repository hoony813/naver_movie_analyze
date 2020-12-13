from flask import render_template,request

from naver_movie.naver_movie_blueprint import naver_movie_blueprint
from naver_movie.model.get_movie_info import get_movie_info

@naver_movie_blueprint.route('/info', methods=['GET', 'POST'])
def naver_movie_info():
    temp1 = id
    _id = request.args.get('id')
    data = get_movie_info(_id)
    return render_template('print_movie_info.html', json_data=data)