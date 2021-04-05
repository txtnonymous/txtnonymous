import re
from os import environ
from flask import Flask
from flask import request
import db, sms

class CustomCommandExecuted(Exception):
    pass

app = Flask(__name__)

tw = sms.Twilio()

def send_message(destination, message):
    app.logger.info("Sent message '%s' to %s", message, destination)
    tw.send_sms(destination, message)

def whats_my_id(frm):
    app.logger.info("whats_my_id called for %s", frm)
    send_message(frm['gid'], 'your txtnonymous id is: #' + frm['tag'])

def delete_my_id(frm):
    app.logger.info("delete_my_id called, removing %s", frm)
    db.delete(frm)
    send_message(frm['gid'], 'your txtnonymous id (#' + frm['tag'] + ') has been deleted.')

special_commands = {
    'whatsmyid': whats_my_id,
    'deletemyid': delete_my_id
}

def get_destination(message, frm):
    hashtag = re.findall('#([a-zA-Z0-9]+)', message)[-1]
    app.logger.info("Hastag: %s", hashtag)
    if hashtag in special_commands.keys():
        app.logger.info("special_command found: %s", hashtag)
        special_commands[hashtag](frm)
        raise CustomCommandExecuted()
    return db.find(tag=hashtag)

def get_forwarded_message(details, frm, to):
    return details.replace(to, frm)

def update_timestamps(arr):
    for u in arr:
        db.extend_timestamp(u)

def on_message_received(from_gid, message):
    app.logger.info("Message from %s: %s", from_gid, message)
    try:
        frm = db.find_or_create(gid=from_gid)
        to = get_destination(message, frm)
    except IndexError:
        app.logger.warn('No destination: use a hastag like #secondfriend')
        send_message(frm['gid'], 'no destination: use a hastag like #secondfriend')
        return
    except db.NotFoundException:
        app.logger.warn('That hashtag is not recognised: check your spelling, but it may have expired.')
        send_message(frm['gid'], 'that hashtag is not recognised: check your spelling, but it may have expired.')
        return
    except CustomCommandExecuted as e:
        return
    except Exception as e:
        app.logger.warn('Caught exception: %s', e)
    send_message(to['gid'], get_forwarded_message(message, frm['tag'], to['tag']))
    update_timestamps([frm['tag'], to['tag']])

tw.init(on_message_received)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/send_msg')
def send_msg():
    from_gid = request.form['From']  
    to_gid = request.form['To']
    message = request.form['Body']
    token = request.form['Token']
    if token != environ['TOKEN']:
        app.logger.warn('Incorrect token: %s', token)
    on_message_received(from_gid, message + " " + to_gid)

@app.route('/receive_msg', methods=['POST'])
def receive_msg():
    message = request.form['Body']
    sender = request.form['From']
    tw.receive_sms(sender, message)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 5000))
    app.run(host=environ.get('HOSTNAME', '0.0.0.0'), port=port)

