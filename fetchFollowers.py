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


print(api.rate_limit_status())  # print info about the rate limits for Tweepy
print(followers_collection)  # print info about the collection

# get all followers of the second user followers (not more than 140k)
numFollowers = 0
for page in tweepy.Cursor(api.followers_ids, screen_name=second_user_handle).pages():
    print("Page exploring")
    for follower in page:
        followers_collection.insert_one({"name": follower, "checked": False})

    numFollowers += len(page)
    print("Added another page of length ", len(page), " followers in followersSecond")
    if numFollowers >= 1000000:  # 1 million cap for big accounts
        break

    if numFollowers % 75000 == 0:
        print("Sleeping for 15 minutes now")
        time.sleep(15 * 60)  # Tweepy crashes when it sleeps on its own so I'll enforce 15 min sleep

print("Finished fetching. Now, let's count who follows ", first_user_handle, ". Run analyzeOverlaps.py for it")