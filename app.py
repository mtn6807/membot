import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = "EAAhSXZBisdTsBAPluTgWitEe2yNASSW3kMmVeioMtCsIcuZBPnWZBbnpn5NitPMpwlhyORfJ8ALIY7sSUdL0kCJyAaP8xIsqRntWxG1GhHBZAkWjk0gwYTVUPrtkewc970APPSMbZCwUTMu1ZBUZASZBW8T9LAp60NHqd3Nj8mMZAUJS3GGFKfTqS"
VERIFY_TOKEN = 'mtn6807'
bot = Bot(ACCESS_TOKEN)
addnextpic = False

@app.route('/', methods=['GET', 'POST'])

def receive_message():
	if request.method == 'GET':
		token_sent = request.args.get("hub.verify_token")
		return verify_fb_token(token_sent)
	else:
		output = request.get_json()
		for event in output['entry']:
			messaging = event['messaging']
			for message in messaging:
				global addnextpic
				if message.get('message'):
					recipient_id = message['sender']['id']
					if message['message'].get('text'):
						message_str =(message['message'].get('text'))
						print(message_str)
						if(message_str=="/add"):
							addnextpic = True

						response_sent_text = get_message()
						send_message(recipient_id, message_str)
					
					if message['message'].get('attachments'):
						if(addnextpic):
							picture = message['message'].get('attachments')
							print(picture)
							imgurl = picture[0].get('payload').get('url')
							
							infile = False
							f = open("pic.txt","r")
							for line in f:
								if(imgurl in line):
									infile = True
							f.close()
							
							if(infile==False):
								print("adding picture "+imgurl)
								f = open("pic.txt","a")
								f.write(imgurl+'\n')
								f.close()
							
							addnextpic = False
    
	return "Message Processed"

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message():
	sample_responses = ["Dawg", "Yo bet", "Homicide is the answer"]
	return random.choice(sample_responses)

def send_message(recipient_id, response):
	bot.send_text_message(recipient_id, response)
	return "success"

if __name__ == '__main__':
    app.run()
