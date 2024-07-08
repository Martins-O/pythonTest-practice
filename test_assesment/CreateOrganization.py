import json

from faker import Faker
import requests

from reusable_files.configFile import baseUrl

fake = Faker()

input_directory = "../reusable_files/authzData.json"
with open(input_directory, "r") as file:
    file_contents = file.read()

try:
    data = json.loads(file_contents)
except json.JSONDecodeError as e:
    raise ValueError(f"Error parsing JSON: {e}")

if not isinstance(data, dict):
    raise ValueError("The parsed data is not a dictionary")

access_token = data["access_token"]


def create_organization(name, website, industry, site_name):
    url = baseUrl + "organization/create/"
    payload = {
        "name": name,
        "organizationLogo": "",
        "website": website,
        "industry": industry,
        "siteName": site_name,
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8"
    }

    try:
        response_data = requests.post(url, data=payload, headers=headers)
        response_data.raise_for_status()
        return response_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response Body: {response_data.text}")  # Add this line to print the response body
        return None
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
        return None


if __name__ == "__main__":
    name_request = fake.first_name()
    print(name_request)
    website_request = fake.url()
    industry_request = fake.bs()
    site_name_request = fake.domain_name()
    response = create_organization(name_request, website_request, industry_request, site_name_request)
    if response:
        print(".... create successful...")
        print(response.json())
    else:
        print("... create failed... ")