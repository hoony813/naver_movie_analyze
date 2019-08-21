from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import pandas as pd
from scipy import stats
import numpy as np
import json
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbProject

data = np.zeros((101,101), dtype=float)
# Json 파일 만들기
# data mean 구하기
# temp_list = db.compare_movie.find({},{'_id':False, 'total_user':False, 'same_user':False})
#
# for x in temp_list:
#     data[x['movie1_id']][x['movie2_id']] = x['prob']
#     data[x['movie2_id']][x['movie1_id']] = x['prob']


data_json = {}
data_json['links'] = []
data_json['nodes'] = []
# temp_list1 = db.movie_info.find({},{'_id':False,'director':False,'actor':False})
# genre_num = [{'title':None, 'group':0},]
# for x in temp_list1:
#     num = -1
#     cnt = 0
#     for y in genre_num:
#         cnt+=1
#         if x['genre'][0] == y['title']:
#             num = y['group']
#     if num == -1:
#         genre_num.append({'title':x['genre'][0],'group':cnt})
#         num = cnt
#     data_json['nodes'].append({
#         'id': x['title'],
#         'group': num
#     })

temp_list = db.compare_movie.find({},{'_id':False, 'total_user':False, 'same_user':False})
check = [0]*101
movie_name = ['']*101
for x in temp_list:
    if x['movie1'] == x['movie2']:
        continue
    y = round(x['prob']*100)
    if y >= 10:
        data_json['links'].append({
            'source' : x['movie1'],
            'target' : x['movie2'],
            'value' : y-5
        })
        check[x['movie1_id']] = 1
        check[x['movie2_id']] = 1
        movie_name[x['movie1_id']] = x['movie1']
        movie_name[x['movie2_id']] = x['movie2']

genre_num = [{'title':None, 'group':0},]
for i,name in zip(check,movie_name):
    if i == 1:
        temp_list1 = db.movie_info.find_one({'title':name},{'_id':False,'total_user':False, 'same_user':False})
        num = -1
        cnt = 0
        for y in genre_num:
            cnt+=1
            if temp_list1['genre'][0] == y['title']:
                num = y['group']
        if num == -1:
           genre_num.append({'title':temp_list1['genre'][0],'group':cnt})
           num = cnt
        data_json['nodes'].append({
                'id': temp_list1['title'],
                'group': num
            })





# json 파일 저장
with open('movie_score_2.json','w',encoding='UTF-8') as outfile:
      json.dump(data_json, outfile, ensure_ascii=False, indent=4)

