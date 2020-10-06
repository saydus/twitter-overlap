import pymongo
import os
from dotenv import load_dotenv
load_dotenv()


first_user_handle = os.getenv("FIRST_USER")
second_user_handle = os.getenv("SECOND_USER")

mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_url = "mongodb+srv://" + mongo_user + ":" + mongo_password +  \
            "@cluster0.ecwwk.mongodb.net/<dbname>?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongo_url)
db = client.twitter_db
followers_collection = db["followers"]


# Statements in console
num_checked = followers_collection.count_documents({first_user_handle + 'Checked': True})
num_overlap = followers_collection.count_documents({first_user_handle: True})
num_of_fails = followers_collection.count_documents({"failed": True})
print("Tweepy failed ", num_of_fails, " times")
print("Followers of ", second_user_handle, " analyzed: ",  num_checked)
print("Overlaps with ", first_user_handle, " found: ", num_overlap)
