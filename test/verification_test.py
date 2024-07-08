# import json
# import unittest
#
# from test_assesment.Verification import mail_verification
#
# input_directory = "../reusable_files/registration_data.json"
# with open(input_directory, "r") as file:
#     file_contents = file.read()
#
# try:
#     data = json.loads(file_contents)
# except json.JSONDecodeError as e:
#     raise ValueError(f"Error parsing JSON: {e}")
#
# if not isinstance(data, dict):
#     raise ValueError("The parsed data is not a dictionary")
#
# correct_email = data["email"]
# correct_token = data["token"]
#
#
# class VerificationTest(unittest.TestCase):
#     def test_correct_token_and_email_Address(self):
#
#         response = mail_verification(correct_email, correct_token)
#
#         self.assertIsNotNone(response, "Response is None")
#         self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")
#
#         api_response_data = response.json()
#
#         self.assertIsInstance(api_response_data, dict, "Response is not a dictionary")
#         self.assertEqual(data.get("body"), "Email Verified Successfully",
#                          f"Unexpected body content: {data.get('body')}")
#
#         print("POST request test passed.")
#
#     def test_invalid_token(self):
#
#         response = mail_verification(correct_email, correct_token)
#         print(response)
#         self.assertIsNotNone(response, "Response is None")
#         self.assertEqual(response.status_code, 400, f"Expected status code 400, but got {response.status_code}")
#
#         api_response_data = response.json()
#
#         self.assertIsInstance(api_response_data, dict, "Response is not a dictionary")
#         self.assertEqual(data.get("message"), "Invalid token",
#                          f"Unexpected body content: {data.get('body')}")
#
#         print("POST request test passed.")
