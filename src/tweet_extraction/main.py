# main.py
# Contains the main code for requesting the Twitter API, handling responses and saving the data

import os
import traceback
import pandas as pd
import json
from twitter_requests import get_all_tweets,  get_location
from utils import get_relevant_data
from config import START_TIME, END_TIME, QUERIES, TWEET_PARAMS, locations_from_api, users_from_api
from time import time, strftime, localtime

not_wb_data = []  # data found to be not from WB
wb_data = []    # data found to be from WB
not_hi_en_bn_data = []  # data not in hi, en, bn

general_data_file = os.getcwd() + "/data/data_file.txt"     # file where logs will eb kept

WB_COUNT = 0
NOT_WB_COUNT = 0
NOT_BN_HI_EN_COUNT = 0
NOT_BN_HI_EN_WB_COUNT = 0
NOT_BN_HI_EN_NOT_WB_COUNT = 0
TOTAL_COUNT = 0

start = time()
exec_start_time = strftime("%H:%M:%S", localtime())
print("Start Time: ", exec_start_time)

f = open(general_data_file, "a")
f.write("----------------------------------------\n")
f.write("Tweets Collected for time range -\n")
f.write("Start Time: " + START_TIME)
f.write("\nEnd Time: " + END_TIME+"\n\n")
f.write("Exec Start Time: " + exec_start_time+"\n")
f.write("Query / topic Tweet Counts: \n\n")

try:
    for topic in QUERIES.keys():    # for every topic in the queries dict

        tweet_id_collection = set()     # maintain a collection of ids (maybe saved if required)
        topic_tweet_count = 0   

        for query in QUERIES[topic]:    # for every query

            TWEET_PARAMS["query"] = query
            query_tweet_count = 0

            next_token = "RANDOM_TOKEN" # starting with a random string (next token for next page of results) for the first request
            while(next_token):  # * next_token -> pagination token; results sorted by time in descending order, first response is the newest

                if(next_token != "RANDOM_TOKEN"):
                    TWEET_PARAMS["next_token"] = next_token

                response = get_all_tweets(TWEET_PARAMS)

                try:
                    next_token = response["meta"]["next_token"]     # next token for next page of results
                except:
                    next_token = None  # if no token is returned, possibly last page

                new_response = {"data": []}  # without the retweeted data, retweets are almost same as original tweets, only they begin with 'RT @username: lorem ipsum ...'
                new_response["meta"] = response["meta"]

                WB_COUNT_initial = len(wb_data)
                NOT_WB_COUNT_initial = len(not_wb_data)
                NOT_BN_HI_EN_COUNT_initial = len(not_hi_en_bn_data)

                RETWEET_COUNT = 0

                if not response:   # if None returned from get_all_tweets() 
                    continue

                for tdata in response["data"]:  # for every tweet data in the response

                    if tdata["text"].startswith("RT"):  # to remove the retweets
                        RETWEET_COUNT += 1
                        continue

                    if tdata["id"] in tweet_id_collection:  # if same tweet was already received earlier, possible when a number of queries were given for the same topic
                        continue

                    tweet_id_collection.add(tdata["id"])

                    new_response["data"].append(tdata)

                    TOTAL_COUNT += 1
                    query_tweet_count += 1
                    topic_tweet_count += 1

                    hi_en_bn = True
                    if tdata["lang"] == "bn":  # bengali text means someone from Bengal
                        tdata["within_wb"] = "y"
                        wb_data.append(get_relevant_data(tdata, topic))
                        continue

                    elif tdata["lang"] not in ["en", "hi"]:  # only hi, en, bn are used
                        # others are collected in a different array
                        hi_en_bn = False
                        # continue

                    loc, is_wb = get_location(tdata, locations_from_api, users_from_api)

                    if is_wb:
                        tdata["within_wb"] = "y"
                        if hi_en_bn:
                            wb_data.append(get_relevant_data(tdata, topic, loc))
                        else:
                            NOT_BN_HI_EN_WB_COUNT += 1
                            not_hi_en_bn_data.append(get_relevant_data(tdata, topic, loc))
                    else:
                        tdata["within_wb"] = "n"
                        if hi_en_bn:
                            not_wb_data.append(get_relevant_data(tdata, topic, loc if loc.strip() else "NOT Recognized"))
                        else:
                            NOT_BN_HI_EN_NOT_WB_COUNT += 1
                            not_hi_en_bn_data.append(get_relevant_data(tdata, topic, loc if loc.strip() else "NOT Recognized"))

                WB_COUNT_final = len(wb_data)
                NOT_WB_COUNT_final = len(not_wb_data)
                NOT_BN_HI_EN_COUNT_final = len(not_hi_en_bn_data)

                WB_COUNT += WB_COUNT_final - WB_COUNT_initial
                NOT_WB_COUNT += NOT_WB_COUNT_final - NOT_WB_COUNT_initial
                NOT_BN_HI_EN_COUNT += NOT_BN_HI_EN_COUNT_final - NOT_BN_HI_EN_COUNT_initial

                new_response["meta"]["final_count"] = len(new_response["data"])
                new_response["meta"]["retweet_count"] = RETWEET_COUNT
                new_response["meta"]["wb_count"] = WB_COUNT_final - WB_COUNT_initial
                new_response["meta"]["NOT_WB_COUNT"] = NOT_WB_COUNT_final - NOT_WB_COUNT_initial
                new_response["meta"]["NOT_BN_HI_EN_COUNT"] = NOT_BN_HI_EN_COUNT_final - NOT_BN_HI_EN_COUNT_initial

                newest_id = response["meta"]["newest_id"]
                oldest_id = response["meta"]["oldest_id"]
                # save the data in a file

                try:
                    os.mkdir(os.getcwd() + f"/data/json/{topic}")
                except FileExistsError:
                    _ = "Already Exists"

                with open(os.getcwd()+f"/data/json/{topic}/{query}_{newest_id}_{oldest_id}.json", "w") as jsonf:
                    json.dump(new_response, jsonf)
                    jsonf.close()

            print(query + " tag done! Time Elapsed: "+str(time()-start))
            f.write("Query Tag " + query + ": " + str(query_tweet_count)+"\n")

        print(topic + " topic done!Time Elapsed: "+str(time()-start)+"\n")
        f.write("topic " + topic + ": " + str(topic_tweet_count)+"\n\n")

except:
    traceback.print_exc()

finally:
    try:
        try:
            pd.read_csv(os.getcwd()+"/data/csv/wb_data.csv").append(wb_data,ignore_index=True).drop_duplicates(subset="id_topic").to_csv(os.getcwd()+"/data/csv/wb_data.csv", index=False)
        except:
            pd.DataFrame(wb_data).drop_duplicates(subset="id_topic").to_csv(os.getcwd()+"/data/csv/wb_data.csv", index=False)

        try:
            pd.read_csv(os.getcwd()+"/data/csv/not_wb_data.csv").append(not_wb_data,ignore_index=True).drop_duplicates(subset="id_topic").to_csv(os.getcwd()+"/data/csv/not_wb_data.csv", index=False)
        except:
            pd.DataFrame(not_wb_data).drop_duplicates(subset="id_topic").to_csv(os.getcwd()+"/data/csv/not_wb_data.csv", index=False)

        try:
            pd.read_csv(os.getcwd()+"/data/csv/not_hi_en_bn_data.csv").append(not_hi_en_bn_data,ignore_index=True).drop_duplicates(subset="id_topic").to_csv(os.getcwd()+"/data/csv/not_hi_en_bn_data.csv", index=False)
        except:
            pd.DataFrame(not_hi_en_bn_data).drop_duplicates(subset="id_topic").to_csv(os.getcwd()+"/data/csv/not_hi_en_bn_data.csv", index=False)

        try:
            pd.read_csv(os.getcwd()+"/data/csv/locations_from_api.csv").append(locations_from_api,ignore_index=True).drop_duplicates(subset="id").to_csv(os.getcwd()+"/data/csv/locations_from_api.csv", index=False)
        except:
            pd.DataFrame(locations_from_api).drop_duplicates(subset="id").to_csv(os.getcwd()+"/data/csv/LOCATIONS_FROM_API.csv", index=False)
        try:
            pd.read_csv(os.getcwd()+"/data/csv/users_from_api.csv").append(users_from_api,ignore_index=True).drop_duplicates(subset="id").to_csv(os.getcwd()+"/data/csv/users_from_api.csv", index=False)
        except:
            pd.DataFrame(users_from_api).drop_duplicates(subset="id").to_csv(os.getcwd()+"/data/csv/users_from_api.csv", index=False)

    finally:
        # logs
        print("Completed!\nTotal Time taken: "+str(time()-start) + "seconds")
        print("End Time: ", strftime("%H:%M:%S", localtime()))

        f.write("Exec End Time: "+strftime("%H:%M:%S", localtime())+"\n")
        f.write("Total tweets: " + str(TOTAL_COUNT)+"\n")
        f.write("WB Count: "+str(WB_COUNT)+"\n")
        f.write("Not WB Count: "+str(NOT_WB_COUNT)+"\n")
        f.write("Not hi_en_bn Count: "+str(NOT_BN_HI_EN_COUNT) + " consisting of in WB: " +
                str(NOT_BN_HI_EN_WB_COUNT) + "  outside WB: " + str(NOT_BN_HI_EN_NOT_WB_COUNT) + "\n")
        f.write("Last Token (if any): " +
                (next_token if next_token else "None"))
        f.write("\nLast query: " + query + "\n")
        f.close()
