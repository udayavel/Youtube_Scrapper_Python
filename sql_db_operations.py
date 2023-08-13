import mysql.connector

def data_to_sql(data):
    conn = mysql.connector.connect(host='localhost', user='root', password='root')
    my_cursor = conn.cursor()
    my_cursor.execute("create database if not exists yt")
    my_cursor.execute(
        "create table if not exists yt.youtubers(video_title varchar(300),comments_count int,likes_count int,video_link varchar(300),video_link_downloaded varchar(300),thumbnail_link varchar(200))")
    my_cursor.execute("insert into yt.youtubers values(%s,%s,%s,%s,%s,%s)",(data['video_title'],data['comments_count'],data['likes_count'],data['video_link'],data['video_link_downloaded'],data['thumbnail_link']))
    conn.commit()

def update_id_to_sql(id,title):
    conn = mysql.connector.connect(host='localhost', user='root', password='root')
    my_cursor = conn.cursor()
    my_cursor.execute("update yt.youtubers set mdb_id= %s where video_title= %s",(id,title))
    conn.commit()








