import pandas as pd
import numpy as np
from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient('localhost', 27017)
db = client.naver_movie


def cal_movie_score():
    col_name = "naver_movie_info"
    movie_lists = list(db.get_collection(col_name).find())
    mongo_cond = []
    for movie in movie_lists:
        doc = dict()
        doc.update({'title':movie['title'],'code':movie['code']})
        mongo_cond.append(doc.copy())
    user_lists = list(db.user_review_list.find({'$or':mongo_cond},{'_id':False,'title':True,'username':True}))
    df = pd.DataFrame(user_lists)
    df['count'] = 1
    table = pd.pivot_table(df,values='count', index=['title'], columns=['username'], aggfunc='count' ,fill_value=0)
    n = len(table.index)

    for i in range(n):
        for j in range(i+1,n):
            doc = dict()
            idx1 = table.index[i]
            idx2 = table.index[j]
            temp1 = table.loc[idx1]
            temp2 = table.loc[idx2]
            total = len(df[(df['title'] == idx1) | (df['title'] == idx2)]['username'].unique())
            results = np.multiply(temp1, temp2)
            doc.update({'movie1':idx1,'movie2':idx2,'score':np.count_nonzero(results == 1),'total':total})
            doc.update({'value':(doc['score']/doc['total']) * 100})
            temp = db.naver_movie_score.find_one({'$or':[{'movie1':idx1,'movie2':idx2},{'movie1':idx2,'movie2':idx1}]})
            if temp == None:
                db.naver_movie_score.insert_one(doc.copy())
            else:
                db.naver_movie_score.update_one({'_id':temp['_id']},{"$set":{'score':doc['score'],'total':doc['total'],'value':doc['value']}})

if __name__ == "__main__":
    cal_movie_score()