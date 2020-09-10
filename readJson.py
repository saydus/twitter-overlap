import json
# change the first part of findOverlap to the following code if you have secondUserFollowers.json
# ready and do not need to retrieve anything else.
data = {}
with open('secondUserFollowers.json', 'w') as outfile:
    json.dump(data, outfile)

followersSecond = data["list"]