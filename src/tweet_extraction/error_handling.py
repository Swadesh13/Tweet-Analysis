# error_handling.py
# Code for handling response errors from Twitter API requests

from time import sleep, strftime, localtime
from requests import Response


def if_continue() -> int:
    '''
        Function that asks the user if continue on error

        Return Values:
        0 -> To Exit
        1 -> Continue without trying
        2 -> Try Again
    '''
    cont = input(f"\nContinue? Y or Try Again (T) or N(to exit): ")
    if cont.strip().lower() == "n":
        return 0
    elif cont.strip().lower() == "y":
        return 1
    elif cont.strip().lower() == "t":
        return 2
    else:
        print("Not Understood! Trying Again.")
        return 2


# ? For error handling when requesting from twitter API
def handle_response_error(res: Response, function_name: str) -> int:
    '''
        Possible errors from Twitter API (V1.1 / V2)

        200 -> Success
        304 -> No data to return
        400 -> Bad Request
        401 -> Unauthorized
        403 -> Forbidden (Request understood, but not accpeted/allowed -> Check response)
        404 -> URI (Resource Not Found)
        429 -> Rate Limit exceeded (in every 15min window)
        500 -> Internal server error (Try again)
        502 -> Bad Gateway (Try again)
        503 -> Service Unavailable (Try again)
        504 -> Gateway Timeout (Try again)

        Args:
        res -> Response Object
        function_name -> Function Name String (only for printing to console)

        Returns a status:
        0 -> Exit
        1 -> Continue without trying again
        2 -> Try again
        3 -> Status 200
    '''
    if res.status_code == 429:  # ? If 429, try automatically again after 1 min
        print(strftime("%H:%M:%S", localtime()))
        print(
            f"Status Code for {function_name} Request: 429 - Too many requests. Waiting for 2 mins and trying again!")
        sleep((60*2+1))
        return 2
    elif res.status_code == 200:
        return 3
    else:  # ? For other status, let user decide
        print(strftime("%H:%M:%S", localtime()))
        print(
            f"Error: Status Code for {function_name} Request: {res.status_code}")
        try:
            print(res.json())
        finally:
            return if_continue()


def check_json(res: Response) -> bool:    # checks if file format is json
    if 'json' in res.headers.get('Content-Type').lower():
        return True
    else:
        print(strftime("%H:%M:%S", localtime()))
        print('Error: Response content is not in JSON format! Content: ',
              res.headers.get('Content-Type'))
        return False
