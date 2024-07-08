import json
import os
import unittest

from faker import Faker

from test_assesment.CreateOrganization import create_organization

fake = Faker()

name = fake.first_name()
website = fake.url()
industry = fake.name()
site_name = fake.domain_name()

output_directory = "../reusable_files"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


class CreateOrganizationTest(unittest.TestCase):

    def test_create_organization_correct_details(self):
        response = create_organization(name, website, industry, site_name)

        with open(os.path.join(output_directory, "OrganizationData.json"), "w") as file:
            json.dump({
                "name": name,
                "site_name": site_name,
                "industry": industry,
                "website": website,
            },
                file, indent=4)

        self.assertIsNotNone(response, f"Response is none")
        self.assertEqual(response.status_code, 200, f"expected status code '200'but got {response.status_code} instead")

        data = response.json()

        print(data)

        self.assertIsInstance(data, dict, f"Response is not a dictionary")
        self.assertEqual(data.get("data"), "Organization successfully created",
                         f"Unexpected body content: {data.get('body')}")
        self.assertEqual(data.get("message"), "", f"Unexpected body content: {data.get('body')}")

    def test_create_organization_already_created_by_the_admin(self):
        response = create_organization(name, website, industry, site_name)

        with open(os.path.join(output_directory, "OrganizationData.json"), "w") as file:
            json.dump({
                "name": name,
                "site_name": site_name,
                "industry": industry,
                "website": website,
            },
                file, indent=4)

        self.assertIsNotNone(response, f"Response is none")
        self.assertEqual(response.status_code, 409, f"expected status code '200'but got {response.status_code} instead")

        data = response.json()

        print(data)

        self.assertIsInstance(data, dict, f"Response is not a dictionary")
        self.assertEqual(data.get("data"), "null", f"Unexpected body content: {data.get('body')}")
        self.assertEqual(data.get("message"), "You should not create more than one organization....",
                         f"Unexpected body content: {data.get('body')}")
