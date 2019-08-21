from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import pandas as pd
from scipy import stats
import numpy as np
import json
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbProject

data = np.zeros((101,101), dtype=float)
# Json 파일 만들기
temp_list = db.compare_movie.find({},{'_id':False, 'total_user':False, 'same_user':False})

for x in temp_list:
    data[x['movie1_id']][x['movie2_id']] = x['prob']
    data[x['movie2_id']][x['movie1_id']] = x['prob']

cnt = 0
data_json = {}
data_json['info'] = []
data_json['links'] = []
data_json['nodes'] = []
temp_list1 = db.movie_info.find({},{'_id':False,'director':False,'actor':False})
genre_num = [{'title':None, 'group':0},]
for x in temp_list1:
    num = -1
    cnt = 0
    for y in genre_num:
        cnt+=1
        if x['genre'][0] == y['title']:
            num = y['group']
    if num == -1:
        num = cnt
    data_json['nodes'].append({
        'id': x['title'],
        'group': num
    })

temp_list = db.compare_movie.find({},{'_id':False, 'total_user':False, 'same_user':False})
cnt1 = 0
for x in temp_list:
    cnt+=1
    data_json['links'].append({
        'source' : x['movie1'],
        'target' : x['movie2'],
        'value' : x['prob']*100
    })


data_json['info'].append({'number_movie':cnt,'score_mean':data.mean()*100})




# json 파일 저장
with open('movie_score_temp.json','w',encoding='UTF-8') as outfile:
      json.dump(data_json, outfile, ensure_ascii=False, indent=4)

