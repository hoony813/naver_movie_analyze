from flask import render_template
from naver_movie.naver_movie_blueprint import naver_movie_blueprint


@naver_movie_blueprint.route('/infos?id1=<path:id1>&id2=<path:id2>&total=<path:total>&same=<path:same>')
def two_movie_infos(id1, id2, total, same):

    return render_template('print_card_info.html',id1=id1,id2=id2,total=total,same=same)
