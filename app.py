from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('nM/+hEvSOI21N9rYuyEgS3SDl7HFA9+aIxgSs1y4lrZpsDMvAsbs1ybQgW2W+XA0mrQ5FTVppUel3YaFA8A2BzHpFBCGPkrMI/xt8L9KBjCInEP9qIka5vuIhDEH11zVVqcXQmGzvQD2civejI2IHgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5f1ac4b5f271615c792c2d898c83940d')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()