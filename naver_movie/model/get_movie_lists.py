from naver_movie import client

def get_movie_lists():
    db = client.db

    col_name = 'naver_movie_info'
    list1 = list(db.get_collection(col_name).find({},{"_id":False}))
    genres = set()
    for a in list1:
        genres.update(a['genre'])
    genres = list(genres)
    json_dict = {'links':[],'nodes':[],'genre_data':[],'data':[]}

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
    return json_dict
