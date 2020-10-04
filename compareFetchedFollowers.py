import pymongo
import os
from dotenv import load_dotenv
load_dotenv()

first_user_handle = os.getenv("FIRST_USER")
second_user_handle = os.getenv("SECOND_USER")

mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_url = "mongodb+srv://" + mongo_user + ":" + mongo_password + \
            "@cluster0.ecwwk.mongodb.net/<dbname>?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongo_url)
db = client.twitter_db
second_followers_collection = db[second_user_handle]
first_followers_collection = db[first_user_handle]


for document in second_followers_collection.find({first_user_handle: {"$exists": False}}):
    if first_followers_collection.find({'name': { "$in": document["name"]}}).count() > 0:
        follows = True
    else:
        follows = False
    second_followers_collection.find_one_and_update({"_id": document["_id"]},
                                                    {"$set": {first_user_handle: follows}})
    first_followers_collection.find_one_and_update({"name": document["name"]},
                                                   {"$set": {second_user_handle: follows}})

overlap = second_followers_collection.find({first_user_handle: True}).count()
print("Number of overlapping followers: ", overlap)