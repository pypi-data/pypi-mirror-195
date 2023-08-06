import requests as http
import json


class users:

    @staticmethod
    def get(client, user_id, fields='', offset=0, count=100):
        return http.get(f'https://{client["instance"]}/method/Users.get?user_ids={user_id}&fields={fields}&offset={offset}&count={count}&access_token={client["token"]}').json()['response']

    @staticmethod
    def get_followers(client, user_id, fields='', offset=0, count=100):
        return http.get(f'https://{client["instance"]}/method/Users.getFollowers?user_id={user_id}&fields={fields}&offset={offset}&count={count}&access_token={client["token"]}').json()['response']

    @staticmethod
    def search(client, q, fields='', offset=0, count=100):
        return http.get(f'https://{client["instance"]}/method/Users.search?q={q}&fields={fields}&offset={offset}&count={count}&access_token={client["token"]}').json()['response']
