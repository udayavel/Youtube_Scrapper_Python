from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
import scrapper as sc
import data_retrieval_from_DB as drd

app = Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def homepage():
    return render_template('index.html')

@app.route('/ytdetails',methods=['GET','POST'])
@cross_origin()
def index():
    if request.method =='POST':
        try:
            sc.scrape_data(r'chromedriver.exe','https://www.youtube.com/@velanvlogs-1476/videos',2)
        except Exception as e:
            print('error occurred!!! '+e)

    dfs = drd.data_from_sql()
    for i in dfs:
        i["video_link"]=i['video_link'].replace("watch?v=","embed/")
        print(i['video_link'].replace("watch?v=","embed/"))


    print(dfs)
    dfm = drd.data_from_mongodb()
    return render_template('results.html',dfs=dfs,dfm=dfm)

if __name__ == '__main__':
    app.run()