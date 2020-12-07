import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime, timedelta
import re
import time
from multiprocessing import Process

client = MongoClient('localhost', 27017)
db = client.naver_movie

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'Cache-Control': 'no-cache', "Pragma": "no-cache"}

def naver_movie_list():
    pattern = re.compile("code=\d+")
    urls = []
    dd = datetime.now() - timedelta(days=1)
    ranking = 1
    for page in range(1,5):
        url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date={}&page={}".format(dd.strftime("%Y%m%d"),page)
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'lxml')

        list_ranking = soup.find("div",id="old_content")
        list_ranking = list_ranking.find('table',class_="list_ranking")
        list_ranking = list_ranking.find("tbody").find_all("tr")
        for tr in list_ranking:
            doc = dict()
            title = tr.find("div",class_="tit5")
            if title == None:
                continue
            title = title.find("a")
            mo = pattern.search(title['href'])
            code = mo.group().replace("code=","")
            doc.update({'ranking':ranking,'title':title['title'],'href':title['href'],"code":code})
            ranking += 1
            urls.append(doc.copy())

    return urls

def user_list_scraping(urls, START, END):
    import math
    urls = urls[START:END]
    BASE_URL = "https://movie.naver.com/"
    for a in urls:
        docs = []
        url = BASE_URL + a['href']
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'lxml')

        total_user = soup.find('div',class_="score_total")
        total_user = total_user.find("strong",class_="total").find_all("em")[-1]
        total_user = int(total_user.get_text().strip().replace(",",""))
        total_page = math.ceil(total_user / 10)
        print(a['title'], total_page)
        flag = True
        for page in range(1, total_page+1):
            url = BASE_URL + 'movie/bi/mi/pointWriteFormList.nhn?code={}&type=after&onlyActualPointYn=N&onlySpoilerPointYn=N&order=newest&page={}'.format(a['code'],str(page))
            data1 = requests.get(url, headers=headers)
            soup1 = BeautifulSoup(data1.text, 'lxml')

            results = soup1.find("div",class_="score_result")
            results = results.find_all('li')
            for li in results:
                doc = dict()
                star = li.find("div",class_="star_score")
                star = int(star.find("em").get_text())

                username = li.find("dl").find('dt').find('span').get_text()
                doc.update(a)
                doc.update({'username':username,'star':star,'url':url})
                temp = db.get_collection(a['title']).find_one({'username':username})
                if temp != None:
                    flag = False
                    break
                docs.append(doc.copy())

            if flag == False:
                break

        db.get_collection(a['title']).insert_many(docs)
        time.sleep(2)

def main():
    urls = naver_movie_list()

    n = len(urls)
    time.sleep(1)

    pr1 = Process(target=user_list_scraping, args=(urls, 0, n // 4))
    pr2 = Process(target=user_list_scraping, args=(urls, n // 4, (n // 4) * 2))
    pr3 = Process(target=user_list_scraping, args=(urls, (n // 4) * 2, (n // 4) * 3))
    pr4 = Process(target=user_list_scraping, args=(urls, (n // 4) * 3, n))
    pr1.start()
    pr2.start()
    pr3.start()
    pr4.start()
    pr1.join()
    pr2.join()
    pr3.join()
    pr4.join()


if __name__ == "__main__":
    st = datetime.now()
    main()
    print("경과 시간: {}".format(datetime.now() - st))