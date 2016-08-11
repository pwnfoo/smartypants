import requests
import json
from collections import Counter
import itertools


class MessageCounter :

    def __init__(self):
        self.count = 0
        self.namemap = dict()
        self.user_count = Counter()
        self.messagemap = dict()
        self.updatemap = dict()
        self.idmap = dict()
        self.name = "MessageCounter"


    def __name__(self):
        return self.name

    def __unicode__(self):
        return self.name.decode('utf-8', errors="ignore")


    def get_messages(self, secret_token):
        msg_url = baseurl = 'https://api.telegram.org/bot'+str(secret_token)+'/GetUpdates'

        response = requests.get(baseurl)

        # Parse the response, convert to a dictionary - ignoring all Unicode errors.
        response_dict = json.loads(response.text.decode('utf-8', errors='ignore'))

        fr = open('dumps.json', 'r')
        history = json.load(fr)

        # If the status is ok, return the result - else print an error.
        try:
            if response_dict['ok'] :
                for msg in response_dict['result']:
                    try:
                        # Edge case detection, where username might not be set.
                        try:
                            username = msg['message']['from']['username']
                        except KeyError:
                            username = msg['message']['from']['first_name']

                        # Map usernames to first name and get the last message
                        self.namemap[username] = msg['message']['from']['first_name']
                        self.messagemap[username] = msg['message']['text']
                        self.idmap[username] = msg['message']['from']['id']
                        self.user_count[username] += 1
                    except KeyError:
                        pass

                for user in history:
                    if history[user] == self.user_count[user]:
                        self.updatemap[user] = False
                    else:
                        self.updatemap[user] = True

                with open('dumps.json', 'w') as fw:
                    json.dump(self.user_count, fw)
                return dict(self.user_count)
            else:
                print "[!] The secret key failed validation"
                return False
        except KeyError as e:
            print "[!] Unable to connect to server"
            return False
