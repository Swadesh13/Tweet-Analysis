# auth.py
# Basic OAuth 1 and 2

import requests
from requests_oauthlib import OAuth1Session

class BearerAuth(requests.auth.AuthBase):
    '''
        Class for Bearer Authentication

        Attributes:
        token - String contain Bearer Authentication
    '''
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class OAuth1(OAuth1Session):
    '''
        Class for OAuth 1

        Attributes:
        tokens - Dict containing atleast client_key and client_secret. May also contain resource_owner and resource_owner_secret keys
    '''
    def __init__(self, tokens: dict):
        self.tokens = tokens
        try:
            if all(token in self.tokens for token in ["client_key", "client_scret", "resource_owner", "resource_owner_secret"]):
                return super().__init__(tokens["client_key"], tokens["client_secret"], tokens["resource_owner_key"], tokens["resource_owner_secret"])
            elif all(token in self.tokens for token in ["client_key", "client_scret"]):
                return super().__init__(tokens["client_key"], tokens["client_secret"])
            else:
                raise KeyError()
        except KeyError:
            print("Require atleast 2 tokens: client_key, client_secret")
            exit()
        except Exception as err:
            print(err)
            exit()
