Twitter Overlap
---
A python script to find the number of overlapping followers between different Twitter users. 
 
The script uses [Tweepy](https://github.com/tweepy/tweepy), and because of this [issue](https://github.com/tweepy/tweepy/issues/617), I had to be a little hacky with timeouts (more about this [here](https://docs.google.com/presentation/d/1O3CEgcAUOC1-aQjZ77A3QbBT_meE4uO_xgbYJGdr9Ns/edit?usp=sharing)).

## Getting Started
To install Tweepy: `pip3 install tweepy`.

Create a `config.yaml` in repo's root to include authentication keys for your Twitter Developer account in the following format:
```yaml
consumer_key: "your_consumer_key"
consumer_secret: "your_consumer_secret"
access_token: "your_access_token"
access_token_secret: "your_access_token_secret"

first_user: "username1"
second_user: "username2"
```
For `second_user`, use username of an account with a smaller amount of followers. The reasoning is explained further.

Repo contains three different approaches to calculate overlaps. 
1. Fetching all follower IDs of both accounts to hashmaps, and tracking same entries.
    * Good for small accounts. Produces an accurate number as a result. 
    * Takes a lot to run on big accounts because of Twitter API's 15-minute cooldown period.
2. Fetching followers of one user (`second_user`) and seeing if any of them are subscribed to the other user (`first_user`). 
    * This is an optimal solution for accounts with very different number of following.
    * The solution in `findOverlap.py` relies on the fact that `second_user` has less subscribers when fetching all of its followers.
    * Still takes time because of Twitter cooldown for fetching subscibtions (or "friends" in Twitter API terms).
3. Web scraping from Twitter's front-end.
    * Does not use Tweepy or Twitter's API, which means no cool-downs (yay!).
    * You would need to provide your Twitter credentials to run it since Twitter requires you to be logged in to see followers.

4. Linear interpolation based on a sample.
    * For the second solution here, I included a cap of 150k followers for the smaller account. This will allow for a reasonable amount of runtime for fetching followers.
    * After calculating the ratio of overlapping followers in a sample, we estimate the following for the whole set of subscribers.
    * Very flexible and close to accurate on a good sample, but never produces the actual result. Hence, good for a quick insight into what the overlap looks like is.

## Other important stuff
Running `findOverlap.py`, you will get a `secondUserFollowers.json` file, containing max 150k (or **all** if you uncomment one if-statement to choose method #2 from above)  followers of one account. I save the file because of Twitter API's limitations, which can result in big wait time if you decide to run script again to fetch followers. 

If you stopped the program while fetching the followers, you can just run `readJson.py` which will get you the result using already fetched and cached followers in `secondUserFollowers.json`. 
