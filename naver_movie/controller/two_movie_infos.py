from flask import render_template, request

from naver_movie.naver_movie_blueprint import naver_movie_blueprint
from naver_movie.model.get_movie_info import get_movie_infos

@naver_movie_blueprint.route('/infos', methods=['GET','POST'])
def two_movie_infos():
    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    total = request.args.get('total')
    same = request.args.get('same')
    data = get_movie_infos(id1,id2)
    return render_template('print_card_info.html',json_data=data,id1=id1,id2=id2,total=total,same=same)
