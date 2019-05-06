import random
from flask import Flask, request
from pymessenger.bot import Bot
import os

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)
addnextpic = False
print(bot)
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
						if("/add" in message_str):
							addnextpic = True
						elif("/memory" in message_str):
							tempimg = get_message()
							send_message(recipient_id,tempimg)
					
					if message['message'].get('attachments'):
						if(addnextpic):
							picture = message['message'].get('attachments')
							
							if(picture[0].get('type')!='image'):
								addnextpic = False
								break

							imgurl = picture[0].get('payload').get('url')
							
							infile = False
							f = open("pic.txt","r")
							for line in f:
								if(imgurl in line):
									infile = True
							f.close()
							
							if(infile==False):
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
	print("getting message...")
	f = open("pic.txt","r")
	lines = 0
	for line in f:
		lines = lines+1
	f.close()
	rline = random.randint(1,lines)-1
	currline = 0
	f = open("pic.txt","r")
	for line in f:
		if(currline==rline):
			f.close()
			return line
		else:
			currline = currline+1
	
def send_message(recipient_id, url):
	print("sending message...")
	bot.send_image_url(recipient_id,url)
	return "success"

if __name__ == '__main__':
    app.run()
