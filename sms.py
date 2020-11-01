import logging
from os import environ
import sys

from twilio.rest import Client

try:
    sid = environ['TWILIO_SID']
    auth = environ['TWILIO_AUTH']
    phone_number = environ['PHONE_NUMBER']
except KeyError:
    logging.error("Expecting the following environment variables to be defined: TWILIO_SID, TWILIO_AUTH, PHONE_NUMBER")
    sys.exit(1)


class Twilio:
    def __init__(self):
        logging.info("Creating twilio REST client with sid=%s, auth=%s", sid, auth)
        self.client = Client(sid, auth)

    def send_sms(self, number, message):
        message = self.client.messages.create(to=number, from_=phone_number, body=message)

    def receive_sms(self):
        if not hasattr(self, '_receive_sms'):
            raise NotImplementedError("You need to call init before receiving messages")
        self._receive_sms()

    def init(self, receive_sms_cb):
        # Sets the receive callback 
        self._receive_sms = receive_sms_cb

if __name__ == "__main__":        
      twilio = Twilio()
      twilio.send_sms(environ['MY_PHONE_NUMBER'], "Hallo Joe")

