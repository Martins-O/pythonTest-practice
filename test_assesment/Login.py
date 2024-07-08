import requests


def login(email, password):
    url = "https://ubuntu.enum.africa/realms/semicolon-delivery/protocol/openid-connect/token"

    payload = {
        "grant_type": "password",
        "client_id": "enum",
        "client_secret": "enum",
        "scope": "offline_access",
        "username": email,
        "password": password
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        # response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        return response
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
        return None


# Example usage:
if __name__ == "__main__":
    email = "kobbiev@mailinator.com"
    password = "Password123$"
    response = login(email, password)
    if response:
        print("Login successful")
        print(response.json())
    else:
        print("Login failed")

# if __name__ == '__main__':
# print(login("968da0b8-3e08-41b5-a528-68e9d27e9a9c@mailslurp.net", "Password321@"))
