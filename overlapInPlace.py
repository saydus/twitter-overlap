import tweepy
import yaml

# Getting access to key's of our Twitter developer account through config.yaml
stream = open("config.yaml", 'r')
dictionary = yaml.load(stream, Loader=yaml.FullLoader)

auth = tweepy.OAuthHandler(dictionary["consumer_key"], dictionary["consumer_secret"])
auth.set_access_token(dictionary["access_token"], dictionary["access_token_secret"])

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


first_user_handle = dictionary["first_user"];
second_user_handle = dictionary["second_user"];

overlaps_found = 0
users_checked = 0

print(api.rate_limit_status())


# Get subscribers of second user one by one check if they follow first_user
# Iterate through followers of the second user in-place and find if they follow first user
for page in tweepy.Cursor(api.followers_ids, screen_name=second_user_handle).pages():
    for userId in page:
        users_checked += 1
        for user in tweepy.Cursor(api.friends, user_id=userId).items():
            if user.screen_name == first_user_handle:
                overlaps_found += 1
                break
    print("Overlaps found: " + str(overlaps_found))
    print("Users checked: " + str(users_checked))

print("Percentage: " + str((overlaps_found / users_checked) * 100))

