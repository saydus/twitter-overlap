Twitter Overlap
---
A python script to find the number of overlapping followers between different Twitter users. 
 
The script uses [tweepy](https://github.com/tweepy/tweepy). Install it by running
`pip install tweepy`.

The `config.yaml` should have authentication keys for your Twitter Developer application in the following format:
```yaml
consumer_key: "your_consumer_key"
consumer_secret: "your_consumer_secret"
access_token: "your_access_token"
access_token_secret: "your_access_token_secret"

first_user: "username1"
second_user: "username2"
```

The repo contains three different approaches to getting the number of overlaps. Details of these appraoches can be found [here](https://docs.google.com/presentation/d/1O3CEgcAUOC1-aQjZ77A3QbBT_meE4uO_xgbYJGdr9Ns/edit?usp=sharing). 

Running `findOverlap.py`, you will get a `secondUserFollowers.json` file, containing 150k followers of one account. I save the file because of Twitter API limitations, which can result in big wait time if you decide to run script again to fetch followers.

If program fails in the second part of checking if every follower from `followersSecond` follows `first_user`, rerun the script by fetching `followerSecond` from the generated `.json` file. 
