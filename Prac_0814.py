import requests
from bs4 import BeautifulSoup
import asyncio
from multiprocessing import Pool
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbProject


movie_list = db.easy_movie_list.find_one({}, {'_id': False})
movies = []
cnt = 0
for mt in movie_list['list']:
    cnt += 1
    user_list = db.movie_user_list.find_one({'title':mt},{'_id':False})
    user_over_4 = []
    for user in user_list['user_list']:
        if int(user['point']) >= 4:
            ok = True
            for i in user_over_4:
                if i == user['userId']:
                    ok = False
                    break
            if ok == True:
                user_over_4.append(user['userId'])
    movie = {'title':mt, 'movie_id':cnt, 'user_list':user_over_4}
    movies.append(movie)





Check = [[0]*111 for i in range(111)]

docs = []
for movie1 in movies:
    for movie2 in movies:
        if movie1 == movie2:
            continue
        movie1_id = movie1['movie_id']
        movie2_id = movie2['movie_id']
        if Check[movie1_id][movie2_id] != 0:
            continue
        Check[movie1_id][movie2_id] = 1
        Check[movie2_id][movie1_id] = 1
        same_user = 0
        index1 = 0
        check1 = [0]*(len(movie1['user_list'])+2)
        check2 = [0]*(len(movie2['user_list'])+2)
        for user_name1 in movie1['user_list']:
            index2 = 0
            for user_name2 in movie2['user_list']:
                if user_name1 == user_name2 and check1[index1] == 0 and check2[index2] == 0:
                    check1[index1] = check2[index2] = 1
                    same_user+=1
                    break
                index2+=1
            index1 += 1
        total_user = len(movie1['user_list'])+len(movie2['user_list'])-same_user
        doc = {'movie1':movie1['title'],'movie2':movie2['title'],'movie1_id':movie1_id,'movie2_id':movie2_id,'total_user':total_user,'same_user':same_user,'prob':float(same_user/total_user)}
        print(doc)
        docs.append(doc)
db.compare_movie.insert_many(docs)






