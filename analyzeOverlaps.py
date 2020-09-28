import tweepy
import time
import pymongo
import os
from dotenv import load_dotenv
load_dotenv()

auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))

# wait_on_rate_limit=True stops the script for some time to wait on Twitter API cooldown
# wait_on_rate_limit_notify will notify us in console if the limit was reached and script is "resting"
api = tweepy.API(auth, timeout=600, retry_count=10, retry_delay=5, retry_errors=set([503]),
                 wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

first_user_handle = os.getenv("FIRST_USER")
second_user_handle = os.getenv("SECOND_USER")

mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_url = "mongodb+srv://" + mongo_user + ":" + mongo_password + \
            "@cluster0.ecwwk.mongodb.net/<dbname>?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongo_url)
db = client.twitter_db
followers_collection = db["followers"]

print(api.rate_limit_status()) # print info about the rate limits for Tweepy
print(followers_collection) # print info about the collection

print("Users checked: " + str(followers_collection.count_documents({first_user_handle + 'Checked': True})))
print("Overlaps found: " + str(followers_collection.count_documents({first_user_handle: True})))

# Iterate through every follower of second user found and see if they follow first used
users_checked = 0  # how many users we will iterate on
num_of_fails = 0 # number of times tweepy fails when fetching followers

for document in followers_collection.find({ first_user_handle + 'Checked': { '$exists': False } }):
    users_checked += 1
    try:
        if api.show_friendship(source_id=document["name"], target_screen_name=first_user_handle)[0].following:
            followers_collection.find_one_and_update({"_id": document["_id"]}, {"$set": {first_user_handle: True}})
    except tweepy.error.TweepError as err:
        print("Failed at some point with tweepy, will just skip this follower: {0}".format(err))
        num_of_fails += 1
        followers_collection.find_one_and_update({"_id": document["_id"]}, {"$set": {"failed": True}})

    followers_collection.find_one_and_update({"_id": document["_id"]}, {"$set": {first_user_handle + 'Checked': True}})

    # Cooldown for 15 mins
    if users_checked % 180 == 0:
        print("Sleeping for 15 minutes now")
        time.sleep(15 * 60)

# Statements in console
num_checked = followers_collection.count_documents({first_user_handle + 'Checked': True})
num_overlap = followers_collection.count_documents({first_user_handle: True})
print("Tweepy failed ", num_of_fails, " times")
print("Users checked: ", num_checked)
print("Overlaps found: ", num_overlap)