import pymongo
import os
import csv
from dotenv import load_dotenv
load_dotenv()


mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_url = "mongodb+srv://" + mongo_user + ":" + mongo_password + \
            "@cluster0.ecwwk.mongodb.net/<dbname>?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongo_url)
db = client.twitter_db
followers_collection = db["followers"]



fields = ['Twitter ID', 'realDonaldTrump', 'SenTedCruz', 'marcorubio', 'JohnKasich', 'JebBush']

# writing to csv file
with open('followersData.csv', 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    for document in followers_collection.find({}):
        twitter_user = []
        twitter_user.append(document['name'])

        if "followsOtherUser" in document:
            twitter_user.append('True')
        else:
            twitter_user.append('False')

        for i in ['SenTedCruz', 'marcorubio', 'JohnKasich', 'JebBush']:
            if i in document:
                twitter_user.append('True')
            else:
                twitter_user.append('False')

        # writing the data rows
        csvwriter.writerow(twitter_user)