import telegram
import os
from mysite.settings import TOKEN
import requests
from .models import Profile


def rassil(bot_message):

    #bot_token = os.environ.get("6387712008:AAFMHf11rHY0Hv3Zl3wqrbYJJqvxzq-1i_w")
    bot_chatID = os.environ.get("external_id")
    send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=HTML&text=' + bot_message

    response = requests.get(send_text)