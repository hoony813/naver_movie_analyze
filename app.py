from flask import Flask, render_template, jsonify, request
import os
import json
app = Flask(__name__)



## HTML을 주는 부분



@app.route('/')
def mypage():

    return render_template('homepage.html')


@app.route('/post', methods=['POST','GET'])
def post():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        temp = request.args.get('id')
        temp1 = 'movie_score_'+temp+'.json'
        return render_template('movie_score.html',num=temp, json=temp1)

@app.route('/info', methods=['POST','GET'])
def movie_info():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        temp1 = request.args.get('id')
        print(temp1)
        return render_template('print_movie_info.html',id=temp1)

@app.route('/infos', methods=['POST','GET'])
def get_info():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        temp1 = request.args.get('id1')
        temp2 = request.args.get('id2')
        print(temp1)
        print(temp2)
        temp3 = request.args.get('total')
        temp4 = request.args.get('same')
        return render_template('print_card_info.html',id1=temp1,id2=temp2,total=temp3,same=temp4)




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)