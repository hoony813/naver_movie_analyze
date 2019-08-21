from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import pandas as pd
from scipy import stats
import numpy as np
import json
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbProject

temp_list1 = db.movie_info.find({},{'_id':False,'director':False,'actor':False})

data_json = {}
data_json['info'] = [{'number':100}]
data_json['movies'] = []

for x in temp_list:

    data_json['movies'].append({
        'name':x['title'],
        'genre':x['genre'][0]
    })

with open('movie_category.json', 'w', encoding='UTF-8') as outfile:
    json.dump(data_json, outfile, ensure_ascii=False, indent=4)