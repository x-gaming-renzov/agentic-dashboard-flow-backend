import pymongo
import dotenv
import os

dotenv.load_dotenv()

def get_mongo_db():
    mongo_db_uri = os.getenv("MONGO_DB_URI")
    mongo_db = pymongo.MongoClient(mongo_db_uri).get_database('charliedemo')
    return mongo_db