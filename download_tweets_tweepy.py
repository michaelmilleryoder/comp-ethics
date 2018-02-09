import os
import tweepy
import pandas as pd
import json
from tqdm import tqdm
import pdb

# # Tweepy from status IDs

# OAuth
keys = pd.read_csv('/usr0/home/mamille2/11-830_data/project/tweepy_oauth.txt', index_col=0)

auth = tweepy.OAuthHandler(keys.loc['consumer_key', 'key'], keys.loc['consumer_secret', 'key'])
auth.set_access_token(keys.loc['access_token', 'key'], keys.loc['access_secret', 'key'])

# Construct the API instance
api = tweepy.API(auth)


# Get ID list
data_fpath = '/usr0/home/mamille2/11-830_data/project/NAACL_SRW_2016.csv'
data = pd.read_csv(data_fpath, header=None)

id_list = data[0].tolist()
print("Saw {} tweets".format(len(id_list)))


# Get tweet objects
outdir = '/usr0/home/mamille2/11-830_data/project/zeerak_naacl'

print("Downloading tweets...")
for i in tqdm(range(len(id_list)//100 + 1)):

    outpath = os.path.join(outdir, '{:05}.json'.format(i))

    if os.path.isfile(outpath):
        continue

    tweet_json_list = []

    try:
        tweets = api.statuses_lookup(id_list[i*100 : (i*100)+100])

    except tweepy.TweepError as e:
        print(e)
        continue

    for t in tweets:
        tweet_json_list.append(t._json)
    
    # Write list out
    with open(outpath, 'w') as f:
        json.dump(tweet_json_list, f)
