from flask import render_template,request

from naver_movie.naver_movie_blueprint import naver_movie_blueprint

@naver_movie_blueprint.route('/info?id=<path:id>')
def naver_movie_info(id):
    temp1 = id
    return render_template('print_movie_info.html',id=temp1)