from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import pya3rt
import requests

app = Flask(__name__)

linebot_api=LineBotApi('buEmr3n5TauytWVl+ndjYNya9s7qH44zZh/VP4o3vRs21ZP4XaDmCJw\
RDHWhFlHAiAbnzt8N5zNU/PHF9U/XTkBibNkTUmtFGn2ovOzUikrvuhhWeClJ9chkCO0j5phKpxQXvM\
FSuVA9JGTwhC/QrAdB04t89/1O/w1cDnyilFU=')
handler=WebhookHandler('34bc19faead58d03c098814966ee0ed9')

@app.route('/callback', methods=['POST'])
def callback():
  signature = request.headers["X-Line-Signature"]
  body = request.get_data(as_text=True)

  try:
    handler.handle(body,signature)
  except InvalidSignatureError:
    abort(400)

  return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  ai_message = talk_ai(event.message.text)
  linebot_api.reply_message(event.reply_token, TextSendMessage(text=str(ai_message)))

def talk_ai(word):
  files = {
    'apikey': (None, 'DZZvp1v3nE7Pt3QSLQNISkcnn8kP9phH'),
    'query': (None, word.encode('utf-8')),
  }

  response = requests.post('https://api.a3rt.recruit.co.jp/talk/v1/smalltalk',\
                           files=files)
  return response.json()['results'][0]['reply']
  

if __name__== '__main__':
  app.run()