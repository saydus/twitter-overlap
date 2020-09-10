import tweepy
import yaml
import json

# Getting access to key's of our Twitter developer account through config.yaml
stream = open("config.yaml", 'r')
dictionary = yaml.load(stream, Loader=yaml.FullLoader)

auth = tweepy.OAuthHandler(dictionary["consumer_key"], dictionary["consumer_secret"])
auth.set_access_token(dictionary["access_token"], dictionary["access_token_secret"])

# wait_on_rate_limit=True stops the script for some time to wait on Twitter API cooldown
# wait_on_rate_limit_notify will notify us in console if the limit was reached and script is "resting"
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


first_user_handle = dictionary["first_user"];
second_user_handle = dictionary["second_user"];



print(api.rate_limit_status())


# get all followers of the second user followers (not more than 140k)
followersSecond = [];
for page in tweepy.Cursor(api.followers_ids, screen_name=second_user_handle).pages():
    followersSecond.extend(page)
    with open('secondUserFollowers.json', 'w') as outfile:
        json.dump({len(followersSecond): followersSecond}, outfile)

    print("Added another page of length ", len(page), ". And overall: ", len(followersSecond), " followers in followersSecond")
    if len(followersSecond) >= 150000: # 140k has a cap of one hour of wait time
        break;

print("Finished doing the fetching. Now, let's count who follows ", first_user_handle)

overlaps_found = 0
users_checked = len(followersSecond)

for userId in followersSecond:
    # see if they are subscribed to user 1
    print(userId)
    if api.show_friendship(source_id=userId, target_screen_name=first_user_handle).is_following:
        overlaps_found += 1;
        print("Found a follower #", overlaps_found)

    # print(api.show_friendship(source_id=userId, target_screen_name=first_user_handle))


print("Overall, we analyzed " + str(users_checked) + " followers of " + second_user_handle + ".")
print("Out of those, " + str(overlaps_found) + " also follow " + first_user_handle)


print("Interpolating, we can estimate " + str(api.get_user(second_user_handle).followers_count * overlaps_found / users_checked) + " of overlapping followers")