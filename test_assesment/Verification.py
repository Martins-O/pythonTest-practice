import os

import requests


def mail_verification(email_address, token):
    url = os.getenv("BASE_URL") + "email/verify"

    payload = {
        "email": email_address,
        "token": token
    }
    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        return response

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None
