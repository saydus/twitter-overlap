import tweepy
import yaml
import json
import time

# Getting access to key's of our Twitter developer account through config.yaml
stream = open("config.yaml", 'r')
dictionary = yaml.load(stream, Loader=yaml.FullLoader)

auth = tweepy.OAuthHandler(dictionary["consumer_key"], dictionary["consumer_secret"])
auth.set_access_token(dictionary["access_token"], dictionary["access_token_secret"])

# wait_on_rate_limit=True stops the script for some time to wait on Twitter API cooldown
# wait_on_rate_limit_notify will notify us in console if the limit was reached and script is "resting"
api = tweepy.API(auth, timeout=600, retry_count=10, retry_delay=5, retry_errors=set([503]),
                 wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


first_user_handle = dictionary["first_user"]
second_user_handle = dictionary["second_user"]



print(api.rate_limit_status())


# --------------------------------------------------------------------------------
# Getting array from a json file
second_user_follower_num = api.get_user(second_user_handle).followers_count
data = {}
with open('secondUserFollowers.json') as json_file:
    data = json.load(json_file)


# get an array of all user ID's
followersSecond = data[list(data.keys())[0]]


# --------------------------------------------------------------------------------
# change the first part of findOverlap to the following code if you have secondUserFollowers.json
# You can also run this script seperately because I included the first part here ^
# ready and do not need to retrieve anything else.


overlaps_found = 0 # to count overlapping followers
users_checked = 0 # how many users we will iterate on

for userId in followersSecond:
    # see if they are subscribed to user 1
    users_checked += 1

    if api.show_friendship(source_id=userId, target_screen_name=first_user_handle)[0].following:
        overlaps_found += 1
    print(str(users_checked) + " iterations estimates " +
          str(second_user_follower_num * overlaps_found / users_checked)
          + " of overlapping followers")

    if users_checked % 180 == 0:
        print("Cooling down for Twitter API for 15 minutes")
        time.sleep(15 * 60)







print("Overall, we analyzed " + str(users_checked) + " followers of " + second_user_handle + ".")
print("Out of those, " + str(overlaps_found) + " also follow " + first_user_handle)


print("Interpolating, we can estimate " +
      str(second_user_follower_num * overlaps_found / users_checked)
      + " of overlapping followers")