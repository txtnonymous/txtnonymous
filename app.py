import os
from flask import Flask

import sms, db

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'


tw = sms.Twilio()

def send_message(destination, message):
    tw.send_sms(destination, message)

def get_destination(message):
    # TODO

def get_forwarded_message(details, from, to):
    # TODO

def update_timestamps(arr):
    for u in arr:
        db.extend_timestamp(u)

def onMessageRecieved(from_gid, message):
    frm = db.findOrCreate(from_gid)
    to = get_destination(message)
    if to == null:
        send_message(frm.gid, 'no destination: use a hastag like #secondfriend')
        return
    send_message(to.gid, get_forwarded_message(details, frm.tag, to.tag))
    update_timestamps([frm.tag, to.tag])


tw.init(onMessageRecieved)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

