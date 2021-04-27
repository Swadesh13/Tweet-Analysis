# utils.py
# Basic utils

import json
import os

def get_creds() -> dict:
    '''
        Get the credentials / tokens from the json file.

        Returns a dict of the tokens found in credentials.json
    '''
    with open(os.path.join(os.getcwd(),"data/credentials.json")) as jsonf:
        creds = json.load(jsonf)
        jsonf.close()

    return creds

def get_relevant_data(tdata: dict, topic: str, location: str="Prob. WB") -> dict:
    '''
        Save the relevant tweet data to a file.
        
        Args:
        tdata - Tweet data
        topic - Topic for which requests are made
        location - location as recognized from Tweet data

        Returns:
        res: Dict of all relevant data
    '''
    res = {}
    res["id_topic"] = tdata["id"]+"_"+topic
    res["tweet_id"] = tdata["id"]
    res["author_id"] = tdata["author_id"]
    res["text"] = tdata["text"]
    res["lang"] = tdata["lang"]
    res["loc"] = location

    return res