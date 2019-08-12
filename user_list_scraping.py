import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbProject                      # 'dbsparta'라는 이름의 db를 만듭니다.

# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
docs = []
movie_title = []
for page_num in range(1,3):
    data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20190806&page='+str(page_num),headers=headers)
    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(data.text, 'html.parser')
    # select : 여러개 select_on : 한개
    tr_result = soup.select('#old_content > table > tbody > tr > td.title > div > a')
    for movie in tr_result:
        doc = {'title':movie.text, 'href':movie['href']}
        docs.append(doc)
        movie_title.append(movie.text)

db.naver_movie_list.insert_many(docs)
dics_temp = {'list':movie_title}
db.easy_movie_list.insert_one(dics_temp)

docs1 = []
for mt in movie_title:
    movie = db.naver_movie_list.find_one({'title': mt},{'_id':False})
    data = requests.get('https://movie.naver.com/' + movie['href'], headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    tr_user_number = soup.select('#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_total > strong > em')
    for number in tr_user_number:
        str1 = number.text.strip()
        usernum_str = str1.replace(',', '')
        usernum = int(usernum_str)
        user_num_page = int(usernum / 10);
        if usernum % 10 != 0:
            user_num_page += 1

    new_str = movie['href']
    code_str = new_str.replace('/movie/bi/mi/basic.nhn?code=', '')

    docs_user_list = []
    for p_num_1 in range(1, user_num_page + 1):
        data = requests.get(
            'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=' + code_str + '&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=' + str(
                p_num_1), headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        for li_num in range(1, 11):
            str_li_num = str(li_num)
            tr_result_user = soup.select(
                'body > div > div > div.score_result > ul > li:nth-child(' + str_li_num + ') > div.score_reple > dl > dt > em:nth-child(1) > a > span')
            tr_user_point = soup.select(
                'body > div > div > div.score_result > ul > li:nth-child(' + str_li_num + ') > div.star_score > em')
            for name, rvpoint in zip(tr_result_user,tr_user_point):
                if name.text != None:
                    dic_temp = {"userId":name.text, "point":rvpoint}
                    docs_user_list.append(dic_temp)

    docs_movie_users={'title':mt,'user_list':docs_user_list}
    docs1.append(docs_movie_users)
    print('{} done!!'.format(mt))


db.movie_user_list.insert_many(docs1)

