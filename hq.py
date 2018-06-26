import os
import json
import requests
import configparser


class HQ:
    def __init__(self, phone_number, bearer_token=None):
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
        # self.my_id = self.get_me()['userId']

    def make_request(self, method, endpoint, params=None, headers=None, payload=None, json=None):
        response = requests.request(method, f'{self.api_base_url}{endpoint}', params=params, headers=headers, data=payload, json=json)
        return response.json()

    def authenticate(self, number):
        json_data = {
            'method': 'sms',
            'phone':  f'+1{number}'
        }
        verification_response = self.make_request('POST', 'verifications', headers=self.headers, json=json_data)
        self.verification_id = verification_response['verificationId']
        return self.verification_id

    def verification(self, sms_code):
        json_data = {
            'code':  sms_code
        }
        verification_sms_response = self.make_request('POST', f'verifications/{self.verification_id}', headers=self.headers, json=json_data)
        self.bearer_token = verification_sms_response["auth"]["accessToken"]
        
        # Bearer token  
        self.headers['Authorization'] = f'Bearer {self.bearer_token}'
        return verification_sms_response

    def is_username_available(self, desired_username):
        json_data = {
            'username': desired_username
        }
        return self.make_request('POST', 'usernames/available', json=json_data, headers=self.headers) == {}

    def set_username(self, desired_username):
        if self.is_username_available(desired_username):

            json_data = {
                "country": "us",
                "language": "en",
                "locale": "US",
                "username": desired_username,
                "verificationId": self.verification_id
            }
            set_username_response = self.make_request('POST', 'users', json=json_data, headers=self.headers)
            self.bearer_token = set_username_response['accessToken']
            self.my_id = set_username_response['userId']
        else:
            raise Exception('Username is not available!')

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

    def get_count_of_friend_requests(self):
        return self.make_request('GET', 'friends/requests/incoming/count', headers=self.headers)

    def get_friend_requests(self):
        return self.make_request('GET', 'friends/requests/incoming', headers=self.headers)

    def friends(self):
        return self.make_request('GET', 'friends', headers=self.headers)

    def get_players_from_contacts(self):
        return self.make_request('GET', 'contacts/players', headers=self.headers)

    def get_nonplayers_from_contacts(self):
        return self.make_request('GET', 'contacts/non-players', headers=self.headers)

    def search_users(self, username_query):
        params = {
            'q': username_query
        }
        return self.make_request('GET', 'users', params=params, headers=self.headers)

    def get_user_info(self, user_id):
        return self.make_request('GET', f'users/{user_id}', headers=self.headers)

    def get_users_status(self, user_id):
        return self.make_request('GET', f'friends/{user_id}/status', headers=self.headers)

    def add_friend(self, user_id):
        headers = {
            'Host':             'api-quiz.hype.space',
            'x-hq-device':      'iPhone6,1',
            'Accept':           '*/*',
            'x-hq-client':      'iOS/1.3.6 b89',
            'Authorization':    f'Bearer {self.bearer_token}',
            'Accept-Encoding':  'gzip, deflate',
            'x-hq-stk':         'MQ==',
            'Accept-Language':  'en-us',
            'Content-Type':     'application/json',
            'User-Agent':       'HQ-iOS/89 CFNetwork/808.2.16 Darwin/16.3.0',
            'Connection':       'keep-alive',
            'x-hq-test-key':     ''
        }
        json_data = {}
        return self.make_request('POST', f'friends/{user_id}/requests', json=json_data, headers=headers)

    def remove_friend_request(self, user_id):
        headers = {
            'Host':             'api-quiz.hype.space',
            'x-hq-device':      'iPhone6,1',
            'Accept':           '*/*',
            'x-hq-client':      'iOS/1.3.6 b89',
            'Authorization':    f'Bearer {self.bearer_token}',
            'Accept-Encoding':  'gzip, deflate',
            'x-hq-stk':         'MQ==',
            'Accept-Language':  'en-us',
            'Content-Type':     'application/json',
            'User-Agent':       'HQ-iOS/89 CFNetwork/808.2.16 Darwin/16.3.0',
            'Connection':       'keep-alive',
            'x-hq-test-key':     ''
        }
        return self.make_request('DELETE', f'friends/{user_id}/requests', headers=headers)


    def block_user(self, user_id):
        headers = {
            'Host':             'api-quiz.hype.space',
            'x-hq-device':      'iPhone6,1',
            'Accept':           '*/*',
            'x-hq-client':      'iOS/1.3.6 b89',
            'Authorization':    f'Bearer {self.bearer_token}',
            'Accept-Encoding':  'gzip, deflate',
            'x-hq-stk':         'MQ==',
            'Accept-Language':  'en-us',
            'Content-Type':     'application/json',
            'User-Agent':       'HQ-iOS/89 CFNetwork/808.2.16 Darwin/16.3.0',
            'Connection':       'keep-alive',
            'x-hq-test-key':     ''
        }
        json_data = {}
        return self.make_request('POST', f'blocks/{user_id}', json=json_data, headers=headers)

    def get_payout(self):
        return self.make_request('GET', 'users/me/payouts', headers=self.headers)


root_directory = os.getcwd()
c = configparser.ConfigParser()
configFilePath = os.path.join(root_directory, 'config.cfg')
c.read(configFilePath)

try:
    bearer_token = c.get('authorization', 'token')
except:
    bearer_token = None
phone_number = str(c.get('verification', 'phone'))
print(json.dumps(HQ(phone_number, bearer_token).get_show_info(), indent=4))
