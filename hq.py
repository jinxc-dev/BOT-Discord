import os
import json
import requests
import configparser
import random
import string


class HQ:
    def __init__(self):
        self.api_base_url = 'https://api-quiz.hype.space/'

        self.headers = {
            'Host':             'api-quiz.hype.space',
            'Content-Type':     'application/json',
            'Accept-Encoding':  'gzip, deflate',
            'User-Agent':       'HQ-iOS/89 CFNetwork/808.2.16 Darwin/16.3.0',
            'Connection':       'keep-alive',
            'x-hq-device':      'iPhone6,1',
            'Accept':           '*/*',
            'Accept-Language':  'en-us',
            'x-hq-client':      'iOS/1.3.6 b89',
            'x-hq-test-key':    ''
        }
        self.my_id = None
        self.bearer_token = None
        self.my_id = None

    def make_request(self, method, endpoint, params=None, headers=None, payload=None, json=None):
        response = requests.request(method, f'{self.api_base_url}{endpoint}', params=params, headers=headers, data=payload, json=json)
        return response.json()

    def authenticate(self, number):
        json_data = {
            'method': 'sms',
            'phone':  number
        }
        verification_response = self.make_request('POST', 'verifications', headers=self.headers, json=json_data)
        print(str(verification_response))
        try:
            self.verification_id = verification_response['verificationId']
            return self.verification_id
        except:
            return "error_phone"

    def verification(self, sms_code):
        json_data = {
            'code':  sms_code
        }
        print(self.verification_id)
        sms_response = self.make_request('POST', f'verifications/{self.verification_id}', headers=self.headers, json=json_data)
        print(str(sms_response))
        try:
            if sms_response["auth"] is None:
                return "new_phone"

            self.bearer_token = sms_response["auth"]["accessToken"]
            # Bearer token  
            self.headers['Authorization'] = f'Bearer {self.bearer_token}'
            return sms_response
        except:
            return "error_sms"

    def is_username_available(self, desired_username):
        json_data = {
            'username': desired_username
        }
        return self.make_request('POST', 'usernames/available', json=json_data, headers=self.headers) == {}

    def create_referral(self, referrer_name):
        user_name = self.generator_name() 
        # if self.is_username_available(user_name):
        json_data = {
            "country": "us",
            "language": "en",
            "locale": "US",
            "username": user_name,
            "referringUsername": referrer_name,
            "verificationId": self.verification_id
        }
        set_username_response = self.make_request('POST', 'users', json=json_data, headers=self.headers)
        print(str(set_username_response))
        if (set_username_response == {}):
            return "error_referral"
        else:
            self.bearer_token = set_username_response['accessToken']
            self.my_id = set_username_response['userId']
            self.headers['Authorization'] = f'Bearer {self.bearer_token}'
            self.make_it_rain()
            return set_username_response
        # else:
        #     return "error_exist_user"
    
    def get_show_info(self):
        params = {'type': 'hq'}
        show_info_response = self.make_request('GET', 'shows/now', params=params, headers=self.headers)
        return show_info_response

    def get_me(self):
        user_response = self.make_request('GET', 'users/me', headers=self.headers)
        return user_response

    def get_leaderboard(self):
        params = {'mode': '1'}
        leaderboard_response = self.make_request('GET', 'users/leaderboard', params=params, headers=self.headers)
        return leaderboard_response

    def add_referral_code(self, referringUsername):
        json_data = {'referringUsername': referringUsername}
        referral_response = self.make_request('PATCH', 'users/me', headers=self.headers, json=json_data)
        return referral_response

    def get_user_info(self, user_id):
        return self.make_request('GET', f'users/{user_id}', headers=self.headers)

    def generator_name(self, size=10):
        return ''.join(random.choice(string.ascii_letters) for n in range(size))
    
    def search_users(self, username_query):
        params = {
            'q': username_query
        }
        return self.make_request('GET', 'users', params=params, headers=self.headers)

    def make_it_rain(self):
        return requests.post("https://api-quiz.hype.space/easter-eggs/makeItRain", headers=self.headers).status_code == 200

    def get_user(self, username):
        users = self.search_users(username)
        try:
            sel_user = users['data']
            if len(sel_user) > 0:
                u_id = sel_user[0]['userId']
                return self.get_user_info(u_id)                
            else:
                return "error_no_user"
        except:
            return "error_auth"
