import pymongo
from psycopg2 import connect
import os, dotenv

dotenv.load_dotenv()

def get_sql_db():
    db = connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
    return db

def execute_sql_query(query : str):
    db = get_sql_db()
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    return data

def get_mongo_db():
    mongo_db_uri = os.getenv("MONGO_DB_URI")
    mongo_db = pymongo.MongoClient(mongo_db_uri)
    return mongo_db