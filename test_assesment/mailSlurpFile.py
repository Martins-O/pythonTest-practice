import re

import mailslurp_client

api_key = "bd0e440c153e1a01388461ec75b668fb2cd44fa1467fc9566d9e3a0b1b280158"
mailslurp_client.configuration.host = 'https://api.mailslurp.com'
configuration = mailslurp_client.Configuration()
configuration.api_key['x-api-key'] = api_key

api_client = mailslurp_client.ApiClient(configuration)


def create_mail_server():
    inbox_controller = mailslurp_client.InboxControllerApi(api_client)
    inbox = inbox_controller.create_inbox()
    return inbox


def wait_for_mail_server(inbox_id):
    wait_for_controller = mailslurp_client.WaitForControllerApi(api_client)
    email_he = wait_for_controller.wait_for_latest_email(
        inbox_id=inbox_id, timeout=6000, unread_only=True
    )

    email_body = email_he.body

    otp_code = re.search(r'<span id="otpInput"[^>]*>(\d+)</span>', email_body).group(1)

    return otp_code


if __name__ == '__main__':
    print(wait_for_mail_server("818bc10e-4461-4735-bf4e-0910cb7577e7"))