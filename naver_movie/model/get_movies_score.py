from naver_movie import client
from datetime import datetime, timedelta

def get_movies_score(movie_id):
    movie_id = str(movie_id)

    db = client.db

    col_name = "naver_movie_info"
    title = db.get_collection(col_name).find_one({'code':movie_id},{'_id':False,'title':True})
    title = title['title']
    col_name = "naver_movie_score"
    list1 = list(db.get_collection(col_name).find({'$or':[{'movie1':title},{'movie2':title}]},{'_id':False}).sort('value',-1).limit(10))
    json_dict = {'links': [], 'nodes': [], 'genre_data': [], 'data': []}
    movie_lists = set()
    for a in list1:
        if a['movie1'] == title:
            s, t = title, a['movie2']
        else:
            s, t = a['movie1'], title
        doc = dict()
        doc.update({'source':s,'target':t,'value':a['value'],'total':a['total'],'same':a['score']})
        json_dict['links'].append(doc.copy())
        movie_lists.add(s)
        movie_lists.add(t)
    movie_lists = list(movie_lists)
    mongo_cond = []
    for movie in movie_lists:
        doc = dict()
        doc.update({'title':movie})
        mongo_cond.append(doc.copy())
    col_name = "naver_movie_info"
    list1 = list(db.get_collection(col_name).find({'$or':mongo_cond}, {'_id': False}))
    genres = set()
    for a in list1:
        genres.update(a['genre'])
    genres = list(genres)

    for a in list1:
        doc = dict()

        doc.update({'id':a['title'],'movie_id':a['code'],'group':genres.index(a['genre'][0])+1,'href':a['href'],'genre':a['genre'],'director':a['director'],
                    'actor':a['actor'],'src':a['src']})
        json_dict['nodes'].append(doc.copy())

    for i, v in enumerate(genres):
        doc = dict()
        doc.update({'title':v,'group':i+1})
        json_dict['genre_data'].append(doc.copy())
    json_dict['data'].append({'movie_n':len(list1),'genre_n':len(genres)})
    print(json_dict)
    return json_dict




