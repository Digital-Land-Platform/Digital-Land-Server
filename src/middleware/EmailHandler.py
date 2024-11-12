import smtplib
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from config.config import Config

image_url = Config.get_env_variable("IMAGE_URL")

class EmailHandler:
    
    def __init__(self, email, password, host, port):
        self.email = email
        self.password = password
        self.host = host
        self.port = port
        
    def send_email(self, invitee_email, invite_url, invitee_name, organization_name):
        try:
            
            sg = sendgrid.SendGridAPIClient(api_key=self.password)
            from_email = Email(self.email)  # Use your verified sender
            to_email = To(invitee_email)  # Change to your recipient
            subject = f"Invitation to verify {organization_name}"
            content = Content(
                        "text/html",
                        f"""
                        <html>
                            <body style="font-family: Arial, sans-serif; color: #333;">
                                <h2>Hello {invitee_name},</h2>
                                <p>You have been invited to verify the organization <strong>{organization_name}</strong>.</p>
                                <p>Please click the button below to continue:</p>
                                <a href="{invite_url}" style="
                                    display: inline-block;
                                    padding: 10px 20px;
                                    font-size: 16px;
                                    color: white;
                                    background-color: #007bff;
                                    text-decoration: none;
                                    border-radius: 5px;
                                ">Verify Now</a>
                                <p style="margin-top: 20px;">
                                    <img src="{image_url}" alt="Organization Logo" style="width: 150px; height: auto;">
                                </p>
                                <p>If you have any questions, please contact us for support.</p>
                                <p>Best regards,<br>Global Real Estate</p>
                            </body>
                        </html>
                        """
                    )
            mail = Mail(from_email, to_email, subject, content)

            # Convert the Mail object to JSON and send it
            sg.client.mail.send.post(request_body=mail.get())
                
        except smtplib.SMTPException as e:
            raise Exception(f"Failed to send email due to SMTP error: {e}")
        
        except Exception as e:
            # Capture other general connection errors
            raise Exception(f"Failed to send email: {e}")
    
 