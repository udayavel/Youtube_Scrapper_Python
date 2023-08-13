import json
import mysql.connector
import pymongo


def data_from_sql():
    mydb=mysql.connector.connect(host='localhost',user='root',password='root',database='yt')
    mycursor=mydb.cursor()
    mycursor.execute("select * from youtubers")
    myresult = mycursor.fetchall()
    dict_result = []
    for m in myresult:
        dict_result.append({"video_title":m[0],"comments_count":m[1],"likes_count":m[2],"video_link":m[3],"thumbnail_link":m[5]})
    return dict_result

def data_from_mongodb():
    mongo_client = pymongo.MongoClient('mongodb+srv://Udayavel:root@cluster0.gqsn3hi.mongodb.net/?retryWrites=true&w=majority')
    mydb=mongo_client['scrapper']
    mycol=mydb['scrape']
    return list(mycol.find())