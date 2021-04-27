# twitter_requests.py
# Requests to the Twitter API

from typing import Union
import requests
from time import strftime, localtime
import traceback
from auth import OAuth1, BearerAuth
from utils import get_creds
from error_handling import handle_response_error, check_json, if_continue
from config import LOCATIONS, URL, USER_PARAMS

__creds__ = get_creds()


def get_all_tweets(params: dict)-> dict:
    '''
        Request to search all tweets API endpoint

        Args:
        params - parameters for the GET Request

        Returns:
        A Dict of JSON response if status code = 200 or
        None, if chosen by user
    '''
    auth = BearerAuth(__creds__["Bearer Token"])
    try:
        res = requests.get(url=URL["all"], params=params, auth=auth)    # GET Request to Twitter search tweet API

        check_res = handle_response_error(res, "GET ALL Tweets")    # Chekck the response status code and proceed accordingly
        if check_res == 0:
            exit()

        elif check_res == 1:
            if(input("Suggested: Try Again. Continuing will skip the current query! Do you want to try again? (y/n): ").strip().lower() == 'n'):
                return None
            else:
                print("Trying Again!")
                return get_all_tweets(params)

        elif check_res == 2:
            print("Trying Again!")
            return get_all_tweets(params)

        elif check_res == 3:
            if check_json(res):     # checking if response is a JSON
                return res.json()
            else:
                cont = if_continue()
                if cont == 0:
                    exit()
                elif cont == 1:
                    if(input("Suggested: Try Again. Continuing skip the current query! Do you want to try again? (y/n): ").strip().lower() == 'n'):
                        return None
                    else:
                        print("Trying Again!")
                        return get_all_tweets(params)
                elif cont == 2:
                    print("Trying Again!")
                    return get_all_tweets(params)

    except Exception as e:  # if requests.get() raises an
        print(strftime("%H:%M:%S", localtime()))
        print("get_all_tweets() Exception raised:")
        print(params)
        print(traceback.print_exc())
        cont = if_continue()
        if cont == 0:
            exit()
        elif cont == 1:
            if(input("Suggested: Try Again. Continuing will skip the current query! Do you want to try again? (y/n): ").strip().lower() == 'n'):
                return None
            else:
                print("Trying Again!")
                return get_all_tweets(params)
        elif cont == 2:
            return get_all_tweets(params)


def get_user(user_id: str, users_from_api: list) -> dict:
    '''
    GET the user from twitter users api

    Args:
    user_id - Twitter ID of the user

    Returns:
    Dict of the JSON response, if status = 200 or,
    Dict of user details manually enetered by the user
    '''
    user_url = URL["users"]+user_id

    for user_data in users_from_api:    # Checks if user details (location) is already saved. Saves multiple requests being made :)
        if user_id == user_data["id"]:
            return user_data

    auth = BearerAuth(__creds__["Bearer Token"])

    try:
        res = requests.get(url=user_url, auth=auth, params=USER_PARAMS)    # GET resquest to Twitter users API

        check_res = handle_response_error(res, "GET User")    # Check the response status code
        if check_res == 0:
            exit()

        elif check_res == 1:
            print(f"Please manually enter the following for id: {user_id}. Enter NA, if not available.\n")  
            # Manually enter the location and description, these are needed for an estimation of the user location 
            loc = input("Location: ")
            desc = input("Description: ")
            keep = input("Save the entered data? (y/n): ").strip().lower()
            if keep == 'y':
                users_from_api.append({"id": user_id, "description": desc, "location": loc})    # Update the list for new users

            return {"id": user_id, "location": loc, "description": desc}

        elif check_res == 2:
            return get_user(user_id)

        elif check_res == 3:
            if check_json(res):     # Check if response is JSON
                resj = res.json()
                try:
                    desc = resj['data']['description']
                except:
                    desc = ''
                try:
                    loc = resj['data']['location']
                except:
                    loc = ''
                users_from_api.append(
                    {"id": user_id, "description": desc, "location": loc})    # Update the list for new users
                return resj
            else:
                cont = if_continue()
                if cont == 0:
                    exit()
                elif cont == 1:
                    print(f"Please manually enter the following for id: {user_id}. Enter NA, if not available.\n")
                    loc = input("Location: ")
                    desc = input("Description: ")
                    keep = input(
                        "Save the entered data? (y/n): ").strip().lower()
                    if keep == 'y':
                        users_from_api.append({"id": user_id, "description": desc, "location": loc})
                    return {"id": user_id, "location": loc, "description": desc}
                elif cont == 2:
                    return get_user(user_id)

    except Exception as e:
        print(strftime("%H:%M:%S", localtime()))
        print("get_user() Error:")
        print(user_id)
        print(traceback.print_exc())
        cont = if_continue()
        if cont == 0:
            exit()
        elif cont == 1:
            print(f"Please manually enter the following for id: {user_id}. Enter NA, if not available.\n")
            loc = input("Location: ")
            desc = input("Description: ")
            keep = input("Save the entered data? (y/n): ").strip().lower()
            if keep == 'y':
                users_from_api.append({"id": user_id, "description": desc, "location": loc})
            return {"id": user_id, "location": loc, "description": desc}
        elif cont == 2:
            return get_user(user_id)


def get_location_from_geo(place_id: str, locations_from_api: list) -> str:
    '''
        GET Request to Twitter V1.1 API Endpoint

        Args:
        place_id - Twitter ID for the geo location
        
        Returns:
        Location obtained from the api or, eneterd by user (if error)
    '''
    for loc_data in locations_from_api:     # First, searching in our saved list of locations
        if loc_data["id"] == place_id:
            return loc_data["location"]

    twitter = OAuth1(__creds__)     #Using OAUth 1 
    try:
        res = twitter.get(f"{URL['geo']}{place_id}.json")  # GET Request to Twitter V1.1 endppint
        twitter.close()

        check_res = handle_response_error(res, "GET Location from Geo")     # Check the status code
        if check_res == 0:
            exit()

        elif check_res == 1:
            loc = input(f"Enter Location for id: {place_id}. Enter NA, if not available: ").strip().lower() # Manually Enter the location
            keep = input("Save the entered data? (y/n): ").strip().lower()
            if keep == 'y':
                locations_from_api.append({"id": place_id, "location": loc})    # save the location correspoding the id
            return loc

        elif check_res == 2:
            print("Trying Again!")
            return get_location_from_geo(place_id)

        elif check_res == 3:
            if check_json(res):
                resj = res.json()
                if len(resj["contained_within"]) > 0:   # Extracting the useful info from the response
                    loc = " ".join((resj["full_name"] + " " +resj["contained_within"][0]["full_name"]).lower().split())
                else:
                    loc = " ".join((resj["full_name"]).lower().split())

                locations_from_api.append({"id": place_id, "location": loc})    # save the location correspoding the id
                return loc

            else:   # if returned response is not a JSON
                cont = if_continue()
                if cont == 0:
                    exit()
                elif cont == 1:
                    loc = input(f"Enter Location for id: {place_id}. Enter NA, if not available: ").strip().lower()
                    keep = input("Save the entered data? (y/n): ").strip().lower()
                    if keep == 'y':
                        locations_from_api.append({"id": place_id, "location": loc})    # save the location correspoding the id
                    return loc
                elif cont == 2:
                    print("Trying Again!")
                    return get_location_from_geo(place_id)

    except Exception as e:  # Catch Exception raised by requests package
        print(strftime("%H:%M:%S", localtime()))
        print("get_location_from_geo() Error:")
        print(place_id)
        print(traceback.print_exc())

        cont = if_continue()
        if cont == 0:
            exit()
        elif cont == 1:
            loc = input(
                f"Enter Location for id: {place_id}. Enter NA, if not available: ").strip().lower()
            keep = input("Save the entered data? (y/n): ").strip().lower()
            if keep == 'y':
                locations_from_api.append({"id": place_id, "location": loc})
            return loc
        elif cont == 2:
            print("Trying Again!")
            return get_location_from_geo(place_id)


def get_location_(user_id: str, users_from_api: list)-> bool:
    '''
        Function that returns obtained locations based on either tweet or user loaction / decription.

        Args:
        user_id - User ID for the person

        Returns:

    '''
    within_wb = False
    loc = ""
    user = get_user(user_id, users_from_api)

    desc_is = True
    try:
        _ = user["description"].lower()
    except:
        desc_is = False

    try:
        loc = " ".join(user["location"].lower().split())
        if loc.strip() == "na":     # if user entered NA for get_user()
            raise Exception
        for l in LOCATIONS:
            if l in loc:
                within_wb = True
                break
    except:
        if desc_is:
            desc = user["description"].lower()
            if(desc):
                for l in LOCATIONS:
                    if l in desc:
                        within_wb = True
                        loc += l + " "

    return loc, within_wb



def get_location(tdata: dict, locations_from_api:list, users_from_api:list) -> Union[str, bool]:
    is_wb = False
    try:
        loc = get_location_from_geo(tdata["geo"]["place_id"], locations_from_api)
        if loc:
            for l in LOCATIONS:
                if l in loc:
                    is_wb = True
    except:
        loc, is_wb = get_location_(tdata["author_id"], users_from_api)

    return loc, is_wb