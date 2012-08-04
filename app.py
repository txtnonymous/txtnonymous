import os, re, db
from flask import Flask
from flask import request
import sms

class CustomCommandExecuted(Exception):
    pass

app = Flask(__name__)

tw = sms.Twilio()

def send_message(destination, message):
    tw.send_sms(destination, message)

def whats_my_id(frm):
    send_message(frm['gid'], 'your txtnonymous id is: #' + frm['tag'])

def delete_my_id(frm):
    db.delete(frm)
    send_message(frm['gid'], 'your txtnonymous id (#' + frm['tag'] + ') has been deleted.')

special_commands = {
    'whatsmyid': whats_my_id,
    'deletemyid': delete_my_id
}

def get_destination(message, frm):
    hashtag = re.findall('\s#([a-zA-Z0-9]+)', message)[-1]
    if hashtag in special_commands.keys():
        special_commands[hashtag](frm)
        raise CustomCommandExecuted()
    return db.find(tag=hashtag)

def get_forwarded_message(details, frm, to):
    return details.replace(to, frm)

def update_timestamps(arr):
    for u in arr:
        db.extend_timestamp(u)

def on_message_recieved(from_gid, message):
    print "Message from ", from_gid, " message: ", message
    frm = db.find_or_create(gid=from_gid)
    try:
        to = get_destination(message, frm)
    except IndexError:
        send_message(frm['gid'], 'no destination: use a hastag like #secondfriend')
        return
    except NotFoundException:
        send_message(frm['gid'], 'that hashtag is not recognised: check your spelling, but it may have expired.')
        return
    except CustomCommandExecuted:
        return
    send_message(to['gid'], get_forwarded_message(message, frm['tag'], to['tag']))
    update_timestamps([frm['tag'], to['tag']])

tw.init(on_message_recieved)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/send_msg')
def send_msg():
    from_gid = request.form['From']  
    to_gid = request.form['To']
    message = request.form['Body']
    token = request.form['Token']
    if token != credentials.token:
        print "Incorrect token"
    on_message_received(from_gid, message + " " + to_gid)

@app.route('/receive_msg', methods=['POST'])
def receive_msg():
    message = request.form['Body']
    sender = request.form['From']
    tw.receive_sms(sender, message)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

