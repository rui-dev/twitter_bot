import base64
import apiclient
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from gmail_auth import create_Gmail_credential

def send_msg_with_file(sender, to, subject, message_text):
    message = MIMEMultipart()
    # set each elementes needed
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(message_text, 'plain', 'utf-8')
    message.attach(msg)

    # encode bytes string
    byte_msg = message.as_string().encode(encoding="UTF-8")
    byte_msg_b64encoded = base64.urlsafe_b64encode(byte_msg)
    str_msg_b64encoded = byte_msg_b64encoded.decode(encoding="UTF-8")
    return {"raw": str_msg_b64encoded}

def gmail_send_message(to, subject, message_text):
  sender = "me"
  service = create_Gmail_credential()
  try:
    result = service.users().messages().send(
      userId=sender,
      body=send_msg_with_file(sender, to, subject, message_text)
    ).execute()
    print("Message Id: {}".format(result["id"]))
  except apiclient.errors.HttpError:
    traceback.print_exc()
