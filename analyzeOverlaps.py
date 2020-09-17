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
followers_collection = db.followers


print(api.rate_limit_status()) # print info about the rate limits for Tweepy
print(followers_collection) # print info about the collection


# Iterate through every follower of second user found and see if they follow first used
second_user_follower_num = api.get_user(second_user_handle).followers_count
overlaps_found = 0  # to count overlapping followers
users_checked = 0  # how many users we will iterate on

for document in followers_collection.find({"checked": False}):
    # see if they are subscribed to user 1
    users_checked += 1

    if api.show_friendship(source_id=document["name"], target_screen_name=first_user_handle)[0].following:
        overlaps_found += 1
        followers_collection.find_one_and_update({"_id": document["_id"]}, {"$set": {"followsOtherUser": True}})

    followers_collection.find_one_and_update({"_id": document["_id"]}, {"$set": {"checked": True}})

    # Cooldown for 15 mins
    if users_checked % 180 == 0:
        print("Sleeping for 15 minutes now")
        time.sleep(15 * 60)


# Statements in console
print("Overall, we analyzed " + str(users_checked) + " followers of " + second_user_handle + ".")
print("Out of those, " + str(overlaps_found) + " also follow " + first_user_handle)

print("Interpolating, we can estimate " +
      str(second_user_follower_num * overlaps_found / users_checked)
      + " of overlapping followers")