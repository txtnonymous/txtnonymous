from os import environ
from twilio.rest import TwilioRestClient
sid = environ['TWILIO_SID']
auth = environ['TWILIO_AUTH']
phone_number = environ['PHONE_NUMBER']

class Twilio:
    def __init__(self):
        print "Creating twilio REST client with sid=%s, auth=%s" % (sid, auth)
        self.client = TwilioRestClient(sid, auth)

    def send_sms(self, number, message):
        message = self.client.sms.messages.create(to = number, from_ = phone_number,
                                       body = message)

    def receive_sms():
      raise NotImplementedError, "You need to call init before receiving messages"

    def init(self, receive_sms_cb):
        # Sets the receive callback 
        self.receive_sms = receive_sms_cb

if __name__ == "__main__":        
      twilio = Twilio()
      twilio.send_sms(environ['MY_PHONE_NUMBER'], "Hallo Joe")

