import base64
import os.path
import smtplib

from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://mail.google.com/']

USER_TOKENS = '../token.json'
CREDENTIALS = '../credentials.json'

def getToken() -> str:
    creds = None

    if os.path.exists(USER_TOKENS):
        creds = Credentials.from_authorized_user_file(USER_TOKENS,SCOPES)
        creds.refresh(Request())

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(USER_TOKENS, 'w') as token:
            token.write(creds.to_json())
    return creds.token

def generate_oauth2_string(username, access_token) -> str:
    auth_string = 'user=' + username + '\1auth=Bearer ' + access_token + '\1\1'
    return base64.b64encode(auth_string.encode('ascii')).decode('ascii')

def send_mail(host, port, subject, message, sender, recipients):
    access_token = getToken()
    auth_string = generate_oauth2_string(sender, access_token)

    message = MIMEText(message)
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = ', '.join(recipients)

    server = smtplib.SMTP(host,port)
    server.starttls()
    server.docmd("AUTH","XOAUTH2 " + auth_string)
    server.sendmail(sender,recipients,message.as_string())
    server.quit()