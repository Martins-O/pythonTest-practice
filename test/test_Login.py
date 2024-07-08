import json
import os
import unittest
from json import JSONDecodeError

from test_assesment.Login import login

input_directory = "../reusable_files/registration_data.json"
with open(input_directory, "r") as file:
    file_contents = file.read()

try:
    data = json.loads(file_contents)
except json.JSONDecodeError as e:
    raise ValueError(f"Error parsing JSON: {e}")

if not isinstance(data, dict):
    raise ValueError("The parsed data is not a dictionary")

correct_email = data["email"]
correct_password = data["password"]


class LoginTest(unittest.TestCase):

    def test_login_with_correct_details(self):
        response = login(correct_email, correct_password)

        self.assertIsNotNone(response, "Response is None")
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}")

        response_data = response.json()

        self.assertIsInstance(response_data, dict, "Response is not a dictionary")

        assert isinstance(response_data.get("access_token"), str)
        output_directory = "../reusable_files"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        with open(os.path.join(output_directory, "authzData.json"), "w") as file:
            json.dump({
                "access_token": response_data.get("access_token"),
                "refresh_token": response_data.get("refresh_token")
            },
                file, indent=4)

        assert "access_token" in response_data
        assert "refresh_token" in response_data
        assert "expires_in" in response_data
        assert "refresh_expires_in" in response_data
        assert "token_type" in response_data
        self.assertEqual(response_data.get("token_type"), "Bearer", f"Excepted 'Bearer' but got {response_data.get("token_type")}")

