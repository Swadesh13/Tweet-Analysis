# config.py
# COnfigurations and variable declarations

import json
import os
import pandas as pd

# Important urls
URL = {}
URL["all"] = "https://api.twitter.com/2/tweets/search/all"
URL["users"] = "https://api.twitter.com/2/users/"   # eg. url is "https://api.twitter.com/2/users/:id", id -> path variable
URL["geo"] = "https://api.twitter.com/1.1/geo/id/"  # eg: url is f"https://api.twitter.com/1.1/geo/id/{id}.json"

# List of possible Locations (not exhaustive list) - Area of Focus was West Bengal
LOCATIONS = ["west bengal", "bengal", "kolkata", "siliguri", "asansol", "durgapur", "howrah", "darjeeling", "kharagpur", "berhampore", "malda", "haldia", "nadia", "cooch behar", "jalpaiguri", "birbhum", "hoogly", "midnapore", "medinipur", "bardhaman"]

# dictionary of quries. 
# Schema is as follows- {"topic": ["string_query1", "string_query2", ...]}
QUERIES = {}

with open(os.getcwd() + "/data/queries.json") as jsonf:
    QUERIES = json.load(jsonf)
    jsonf.close()

# Start and End time for the tweets
START_TIME = "2021-03-30T10:00:00Z"
END_TIME = "2021-03-30T14:00:00Z"

# Parameters to be passed to search tweets API
TWEET_PARAMS = {
    "max_results": 500,
    "tweet.fields": "author_id,context_annotations,geo,created_at,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,source,text",
    "start_time": START_TIME,
    "end_time": END_TIME,
}

# Parameters to be passed to get users API
USER_PARAMS = {
    "user.fields": "created_at,description,location,name,username,public_metrics,verified"
}

# Get Locations and Users data from previously saved csv file
# * Location Schema - {"id":"eg_id", "location": "eg_loc"}
try:
    locations_from_api = json.loads(pd.read_csv(os.getcwd() + "/data/locations_from_api.csv", index_col="id").to_json(orient="table"))["data"]
except:
    locations_from_api = []

# * User Schema - {"id":"eg_id", "description": "eg_desc", "location": "eg_loc"}
try:
    users_from_api = json.loads(pd.read_csv(os.getcwd() + "/data/users_from_api.csv", index_col="id").to_json(orient="table"))["data"]
except:
    users_from_api = []
