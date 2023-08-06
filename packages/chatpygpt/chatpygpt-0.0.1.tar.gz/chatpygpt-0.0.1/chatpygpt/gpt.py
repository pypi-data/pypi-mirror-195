from urllib import response
import openai 
import pandas 
import sqlite3 
import json
import os 
import requests




class Gpt(): 
    def __init__(self): 
        self.set_api_key()


    def set_api_key(self): 
        if os.path.exists('creds.json'): 
            with open("creds.json", "r") as f:
                self.api_key = json.load(f)['api_key']
        else: 
            self.api_key = input('What\'s your API key? (press enter to validate) \nYou can find it at: https://platform.openai.com/account/api-keys\n')
            with open("creds.json", "r") as f:
                json.dump({'api_key': self.api_key}, f)

        self.check_valid_api_key()



    def check_valid_api_key(self): 
        '''Makes sure that the api key provided is valid by making a simple request. 
        '''

        response = self.request(data={'messages': [{'role': 'user', 'content': 'hi'}]})
        # print(response.status_code)
        # print(response.json())


        if response.status_code != 200: 
            raise Exception(f'Request failed with status code {response.status_code}\n{response.json()}')



    
    def request(self, data): 
        '''Makes a request to Open AI'''

        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        data = {
            'model': 'gpt-3.-turbo',
            'messages': [{'role': 'user', 'content': 'say hi to my girlfriend, her name is Julie and she\'s rad.'}, 
                         {'role': 'assistant', 'content': '\n\nHello Rad, it\'s nice to "meet" you! Your name is very cool and it sounds like you\'re an awesome person.'}, 
                         {'role': 'user', 'content': 'thanks, whats her name? i game it to you a message before'}]
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response



    
    def new_conversation(self): 
        '''Reset some parameters like conversation id and stuff'''










Gpt()