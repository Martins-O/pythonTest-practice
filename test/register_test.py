import json
import os
import unittest

from faker import Faker
from dotenv import load_dotenv
from test_assesment.mailSlurpFile import create_mail_server, wait_for_mail_server
from test_assesment.Register import registration
from test_assesment.Verification import mail_verification

load_dotenv()

fake = Faker()

email = create_mail_server().email_address
email_id = email.split('@')[0]
password = "Password321@"
first_name = fake.first_name()
last_name = fake.last_name()


class RegistrationTest(unittest.TestCase):

    def test_correct_details(self):
        response = registration(email, password, first_name, last_name)
        print(email)

        output_directory = "../reusable_files"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        with open(os.path.join(output_directory, "registration_data.json"), "w") as file:
            json.dump({
                "email_id": email_id,
                "email": email,
                "password": password,
                "firstName": first_name,
                "lastName": last_name,
                "organizationType": "INSTITUTION",
            },
                file, indent=4)

        self.assertIsNotNone(response, "Response is None")
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")

        data = response.json()

        self.assertIsInstance(data, dict, "Response is not a dictionary")
        self.assertEqual(data.get("body"), "User Registered Successfully",
                         f"Unexpected body content: {data.get('body')}")

        print("Register request test passed.")
        verify_response = mail_verification(email, wait_for_mail_server(email_id))
        print(email)

        self.assertIsNotNone(verify_response, "Response is None")
        self.assertEqual(verify_response.status_code, 200, f"Expected status code 200, but got {verify_response.status_code}")

        api_response_data = verify_response.json()

        self.assertIsInstance(api_response_data, dict, "Response is not a dictionary")
        self.assertEqual(api_response_data.get("body"), "Email Verified Successfully",
                         f"Unexpected body content: {api_response_data.get('body')}")

        print("Verification request test passed.")

    def test_incorrect_email(self):

        email_incorrect = "email.gmail"
        password_incorrect = "Password321@"
        first_name_incorrect = "John"
        last_name_incorrect = "Doe"

        response = registration(email_incorrect, password_incorrect, first_name_incorrect, last_name_incorrect)

        self.assertIsNotNone(response, "Response is None")
        self.assertEqual(response.status_code, 400, "Expected status code 400, but got {response.status_code}")

        try:
            data = response.json()
        except ValueError:
            self.fail("Failed to decode JSON from response.")

        self.assertIn("message", data, "Expected 'message' key in response")
        self.assertIn("email", data["message"], "Expected 'email' key in message")
        self.assertEqual(data["message"]["email"], "Invalid Email Address", "Unexpected error message")
        self.assertEqual(data["httpStatus"], "BAD_REQUEST", "Unexpected httpStatus")

    def test_incorrect_firstName(self):

        password_incorrect = "Password321@"
        first_name_incorrect = 'John123#@'
        last_name_incorrect = "Doe"

        response = registration(email, password_incorrect, first_name_incorrect, last_name_incorrect)

        self.assertIsNotNone(response, "Response is None")
        self.assertEqual(response.status_code, 200, "Expected status code 400, but got {response.status_code}")

        try:
            data = response.json()
        except ValueError:
            self.fail("Failed to decode JSON from response.")

        self.assertIn("message", data, "Expected 'message' key in response")
        self.assertIn("firstName", data["message"], "Expected 'firstName' key in message")
        self.assertEqual(data["message"]["firstName"], "Name should not contain numbers", "Unexpected error message")
        self.assertEqual(data["httpStatus"], "BAD_REQUEST", "Unexpected httpStatus")

    def test_incorrect_lastName(self):
        password_incorrect = "Password321@"
        last_name_incorrect = 'John123#@'
        first_name_incorrect = "Doe"

        response = registration(email, password_incorrect, first_name_incorrect, last_name_incorrect)

        self.assertIsNotNone(response, "Response is None")
        self.assertEqual(response.status_code, 400, "Expected status code 400, but got {response.status_code}")

        try:
            data = response.json()
        except ValueError:
            self.fail("Failed to decode JSON from response.")

        self.assertIn("message", data, "Expected 'message' key in response")
        self.assertIn("lastName", data["message"], "Expected 'lastName' key in message")
        self.assertEqual(data["message"]["lastName"], "Name should not contain numbers", "Unexpected error message")
        self.assertEqual(data["httpStatus"], "BAD_REQUEST", "Unexpected httpStatus")

    def test_incorrect_password(self):
        password_incorrect = "Password@"
        last_name_incorrect = 'John'
        first_name_incorrect = "Doe"

        response = registration(email, password_incorrect, first_name_incorrect, last_name_incorrect)

        self.assertIsNotNone(response, "Response is None")
        self.assertEqual(response.status_code, 400, "Expected status code 400, but got {response.status_code}")

        try:
            data = response.json()
        except ValueError:
            self.fail("Failed to decode JSON from response.")

        self.assertIn("message", data, "Expected 'message' key in response")
        self.assertIn("password", data["message"], "Expected 'password' key in message")
        self.assertEqual(data["message"]["password"], "Invalid Password. Password must contain at least one lowercase "
                                                      "letter, one uppercase, one digit, one special character from "
                                                      "the set @$!%*?& and be at least 8 characters long",
                         "Unexpected error message")
        self.assertEqual(data["httpStatus"], "BAD_REQUEST", "Unexpected httpStatus")
