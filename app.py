import os, re
from flask import Flask
from flask import request

import sms

app = Flask(__name__)
tw = sms.Twilio()

def receive_sms(sender, message):
    print "Message from ", sender, " message: ", message
tw.init(receive_sms)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/receive_sms', methods=['POST'])
def receive_sms():
    message = request.form['Body']
    sender = request.form['From']
    import IPython
    IPython.embed()
    tw.receive_sms(sender, message)

def send_message(destination, message):
    tw.send_sms(destination, message)

def get_destination(message):
    return db.find(re.findall('\s#([a-zA-Z][a-zA-Z0-9]+)', message)[-1])

def get_forwarded_message(details, frm, to):
    return details.replace(to, frm)

def update_timestamps(arr):
    for u in arr:
        db.extend_timestamp(u)

def on_message_recieved(from_gid, message):
    frm = db.find_or_create(from_gid)
    try:
        to = get_destination(message)
    except IndexError, Exception:
        send_message(frm.gid, 'no destination: use a hastag like #secondfriend')
        return
    send_message(to.gid, get_forwarded_message(details, frm.tag, to.tag))
    update_timestamps([frm.tag, to.tag])


tw.init(on_message_recieved)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

