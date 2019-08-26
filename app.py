from flask import Flask, render_template, jsonify, request
import os
import json
app = Flask(__name__)



## HTML을 주는 부분
@app.route('/')
def home():
    return 'This is Home!'



@app.route('/mypage')
def mypage():

    return render_template('prac_menu.html')



@app.route('/post', methods=['POST','GET'])
def post():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        temp = request.args.get('id')
        #1
        temp1 = 'movie_score_'+temp+'.json'

        return render_template('movie_score.html',num=temp, temp1=temp1)




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)