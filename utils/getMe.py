import requests
import json


class GetBotDetails :

    def __init__(self):
        self.id = 0
        self.name = None
        self.username = None


    def get_server_response(self, secret_token):
        # Set the baseurl with the secret_token
        baseurl = 'https://api.telegram.org/bot'+str(secret_token)+'/getMe'

        # Get response from server using a GET request
        response = requests.get(baseurl)

        # Parse the response, convert to a dictionary - ignoring all Unicode errors.
        response_dict = json.loads(response.text.decode('utf-8', errors='ignore'))

        # If the status is ok, return the result - else print an error.
        try:
            if response_dict['ok'] :
                self.username = response_dict['result']['username']
                self.name = response_dict['result']['first_name']
                self.id = response_dict['result']['id']
                return True
            else:
                print "[!] The secret key failed validation"
                return False
        except KeyError as e:
            print "[!] Unable to connect to server"
            return False
