from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEv\
ent, FlexSendMessage, StickerSendMessage
import requests

app = Flask(__name__)

line_bot_api=LineBotApi('buEmr3n5TauytWVl+ndjYNya9s7qH44zZh/VP4o3vRs21ZP4XaDmCJw\
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
def handle_text_message(event):
    # メッセージでもテキストの場合はオウム返しする
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


if __name__== '__main__':
  app.run()
