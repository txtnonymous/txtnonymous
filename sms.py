import os
from twilio.rest import TwilioRestClient
try:
    import credentials
except:
    print "No credentials module, use environment variables"

class Twilio:
    def __init__(self):
        self.client = TwilioRestClient(os.environ.get('TWILIO_SID', credentials.sid),
                os.environ.get('TWILIO_AUTH', credentials.auth))

    def send_sms(self, number, message):
        message = self.client.sms.messages.create(to = number, from_ = credentials.phone_number,
                                       body = message)

    def receive_sms():
      raise NotImplementedError, "You need to call init before receiving messages"

    def init(self, receive_sms_cb):
        # Sets the receive callback 
        self.receive_sms = receive_sms_cb

if __name__ == "__main__":        
      twilio = Twilio()
      twilio.send_sms(credentials.joe_phone_number, "Hallo Joe")

