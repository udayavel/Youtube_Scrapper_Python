import pymongo
import sql_db_operations as sq

def insert_into_mongo(data):
    myclient = pymongo.MongoClient(
        'mongodb+srv://Udayavel:root@cluster0.gqsn3hi.mongodb.net/?retryWrites=true&w=majority')
    mydb = myclient['scrapper']
    mycollection = mydb['scrape']
    inserted_record = mycollection.insert_one(data)
    id = str(inserted_record.inserted_id)
    # updating mongodb id to sql for mapping
    # sq.update_id_to_sql(id,data['video_title'])
    # mycollection.update_one({"video_title":data['video_title']},{"$rename":{"comments":id}})






