from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, FlexSendMessage, StickerSendMessage
import pya3rt
import requests
import json
import random

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
#友達追加時
@handler.add(FollowEvent)
def handle_follow(event):
    with open('./saisyohaguu_message.json') as f:
        saisyohaguu_message = json.load(f)
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text='最初はぐー', contents=saisyohaguu_message)
    )

#設定されていない場合の返信
@handler.default()
def default(event):
    with open('./saisyohaguu_message.json') as f:
        saisyohaguu_message = json.load(f)
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(package_id='2', sticker_id=random.choice(['152', '18', '25', '173', '524']))
    )

#メッセージを受信した場合
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  request_message = event.message.text
  if request_message == 'じゃんけん' or request_message == 'ぐー' or\
   request_message == 'ちょき' or request_message == 'ぱー' or\
    request_message == 'ジャンケン' or request_message == 'グー' or\
    request_message == 'チョキ' or request_message == 'パー' :
    bot_answer = random.choice(['ぐー', 'ちょき', 'ぱー'])
    with open('./saisyohaguu_message.json') as f:
        saisyohaguu_message = json.load(f)
    with open('./aikode_message.json') as f:
        aikode_message = json.load(f)
    reply_messages = []
    win_reply_message = [TextSendMessage(text='私の勝ちです')]
    win_reply_message.append(StickerSendMessage(package_id='1', sticker_id=random.choice(['106', '407', '125', '100', '110'])))
    lose_reply_message = [TextSendMessage(text='私の負けです')]
    lose_reply_message.append(StickerSendMessage(package_id='2', sticker_id=random.choice(['152', '18', '25', '173', '524'])))
    draw_reply_message = [FlexSendMessage(alt_text='あいこで', contents=aikode_message)]
    if request_message == 'ぐー' or request_message == 'グー' :
        reply_messages.append(TextSendMessage(text=bot_answer))
        if bot_answer == 'ぐー':
            reply_messages.extend(draw_reply_message)
        elif bot_answer == 'ちょき':
            reply_messages.extend(lose_reply_message)
        elif bot_answer == 'ぱー':
            reply_messages.extend(win_reply_message)
    elif request_message == 'ちょき' or request_message == 'チョキ' :
        reply_messages.append(TextSendMessage(text=bot_answer))
        if bot_answer == 'ぐー':
            reply_messages.extend(win_reply_message)
        elif bot_answer == 'ちょき':
            reply_messages.extend(draw_reply_message)
        elif bot_answer == 'ぱー':
            reply_messages.extend(lose_reply_message)
    elif request_message == 'ぱー' or request_message == 'パー' :
        reply_messages.append(TextSendMessage(text=bot_answer))
        if bot_answer == 'ぐー':
            reply_messages.extend(lose_reply_message)
        elif bot_answer == 'ちょき':
            reply_messages.extend(win_reply_message)
        elif bot_answer == 'ぱー':
            reply_messages.extend(draw_reply_message)
    elif request_message == 'じゃんけん' or request_message == 'ジャンケン':
        reply_messages.append(FlexSendMessage(alt_text='最初はぐー', contents=saisyohaguu_message))
    line_bot_api.reply_message(event.reply_token, reply_messages)
  else:
      ai_message = talk_ai(event.message.text)
      line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(ai_message)))

#AIメッセージ取得
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