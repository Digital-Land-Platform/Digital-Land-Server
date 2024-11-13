import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

try:
    sg = sendgrid.SendGridAPIClient(api_key="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")
    from_email = Email("henokmac63@gmail.com")  # Use your verified sender
    to_email = To("a99li00a99@gmail.com")  # Change to your recipient
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, to_email, subject, content)

    # Convert the Mail object to JSON and send it
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print("An error occurred:", str(e))
