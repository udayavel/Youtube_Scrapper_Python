import mysql.connector
import pymongo


# deleting data from SQL
mydb = mysql.connector.connect(host='localhost',user='root',password='root',database='yt')
mycursor = mydb.cursor()
mycursor.execute("delete from youtubers")
mydb.commit()

myclient = pymongo.MongoClient(
    'mongodb+srv://Udayavel:root@cluster0.gqsn3hi.mongodb.net/?retryWrites=true&w=majority')
mydb = myclient['scrapper']
mycollection = mydb['scrape']
mycollection.delete_many({})