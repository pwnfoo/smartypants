import requests
import json
from collections import Counter
import itertools


class MessageSender :

    def __init__(self, userid):
        self.userid = userid
        self.values = dict()


    def SendMessage(self, secret_token, text):
        baseurl = 'https://api.telegram.org/bot'+str(secret_token)+'/SendMessage'
        self.values['chat_id'] = self.userid
        self.values['text'] = text
        response = requests.get(baseurl, params=self.values)
