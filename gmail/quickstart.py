from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import base64
import mimetypes

from contacts import jake, jake_text, alayne, chov, chov_text

from datetime import datetime

import math

# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SCOPES = ['https://mail.google.com/']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    sender = "jake.bot.anderson@gmail.com"
    to_myself = "jaokea@gmail.com"
    to_myself_text = "9496805085@vtext.com"
    subject = "Message from Jakebot!"
    message_text =  """Hi! I'm Jakebot, and just wanted to say hi. \n\n-Jakebot
                    """
    message_chov =  """Good luck on your interview! \n -Jakebot
                    """
    message = create_message(sender, to_myself, subject, message_chov)
    send_message(service, "me", message)

    message2 = create_message(sender, to_myself_text, subject, message_chov)
    send_message(service, "me", message2)

    file_path = "jakebot.png"
    message3 = create_message_with_attachment(sender, to_myself, subject, message_chov, file_path)
    send_message(service, "me", message3)

    message3 = create_message_with_attachment(sender, to_myself_text, subject, message_chov, file_path)
    send_message(service, "me", message3)


    
def create_message_with_attachment(
    sender, to, subject, message_text, file):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(file, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def create_message(sender, to, subject, message_text):
    """Create a message for an email.
    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
        print('Message Id: {}'.format(message['id']))
        return message
    except Exception as e: 
        print('An error occurred: {}'.format(e))

def make_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def send_message_on_fly(to, subject, message_text):
    creds = make_credentials()
    service = build('gmail', 'v1', credentials=creds)

    sender = "jake.bot.anderson@gmail.com"
    message = create_message(sender, to, subject, message_text)
    send_message(service, "me", message)

def time_remaining():
    # datetime object containing current date and time
    now = datetime.now()
    interview_time = datetime(2020,11,19,12,0,0,0)
    time_diff = interview_time - now    
    seconds_remaining = time_diff.seconds
    minutes_remaining = math.floor(seconds_remaining/60)
    time_diff_string = "{} seconds, or roughly {} minutes".format(seconds_remaining,minutes_remaining)
    return time_diff_string
 

if __name__ == '__main__':
    # main()
    subject, message_text =  (  "Message from Jakebot", 
                                "Hi! Good luck on your interview today! You still have {} to prepare!  \n-Jakebot".format(time_remaining()))
    send_message_on_fly(chov_text, subject, message_text)
    send_message_on_fly(jake_text, subject, message_text)

