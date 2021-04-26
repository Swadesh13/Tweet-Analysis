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