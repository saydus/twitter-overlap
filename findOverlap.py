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
api = tweepy.API(auth, timeout=600, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

first_user_handle = dictionary["first_user"]
second_user_handle = dictionary["second_user"]

print(api.rate_limit_status())

# get all followers of the second user followers (not more than 140k)
followersSecond = [];
for page in tweepy.Cursor(api.followers_ids, screen_name=second_user_handle).pages():
    followersSecond.extend(page)
    with open('secondUserFollowers.json', 'w') as outfile: # TODO: dump followers to Mongo here
        json.dump({len(followersSecond): followersSecond}, outfile)

    print("Added another page of length ", len(page), "And overall: ", len(followersSecond),
          " followers in followersSecond")
    if len(followersSecond) >= 150000:  # 150k has a cap of one hour of wait time, comment out if you want full
        break

    if len(followersSecond) % 75000 == 0:
        time.sleep(15 * 60)  # tweepy crashes when it sleeps on its own so I'll enforce 15 min sleep

print("Finished fetching. Now, let's count who follows ", first_user_handle)


# Iterate through every follower of second user found and see if they follow first used
second_user_follower_num = api.get_user(second_user_handle).followers_count
overlaps_found = 0  # to count overlapping followers
users_checked = 0  # how many users we will iterate on

for userId in followersSecond:
    # see if they are subscribed to user 1
    users_checked += 1

    if api.show_friendship(source_id=userId, target_screen_name=first_user_handle)[0].following:
        overlaps_found += 1 # TODO: change these values in mongo for every follower
    print(str(users_checked) + " iterations estimates " +
          str(second_user_follower_num * overlaps_found / users_checked)
          + " of overlapping followers") # TODO: change these values in mongo for every follower

    if users_checked % 180 == 0:
        print("Cooling down for Twitter API:", time.time())
        time.sleep(15 * 60)


# Statements in console
print("Overall, we analyzed " + str(users_checked) + " followers of " + second_user_handle + ".")
print("Out of those, " + str(overlaps_found) + " also follow " + first_user_handle)

print("Interpolating, we can estimate " +
      str(second_user_follower_num * overlaps_found / users_checked)
      + " of overlapping followers")
