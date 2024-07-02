import requests

base_url = "https://api-systest.enum.africa/api/v2/"


def registration(email, password, first_name, last_name):

    url = base_url + "user/organization-signup"

    payload = {
        "email": email,
        "password": password,
        "firstName": first_name,
        "lastName": last_name,
        "organizationType": "INSTITUTION"
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
