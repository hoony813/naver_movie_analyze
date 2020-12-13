from naver_movie import client

def get_movie_info(_id):
    db = client.db
    col_name = "naver_movie_info"
    info = db.get_collection(col_name).find_one({'title': _id}, {'_id': False})

    return info


def get_movie_infos(id1, id2):
    db = client.db
    col_name = "naver_movie_info"

    infos = {}
    temp = db.get_collection(col_name).find_one({'title':id1},{"_id":False})
    infos[id1] = temp
    temp = db.get_collection(col_name).find_one({'title':id2},{"_id":False})
    infos[id2] = temp

    return infos
