import requests as http
import json


class groups:

    @staticmethod
    def get(client, user_id, fields='', offset=0, count=100):
        return http.get(f'https://{client["instance"]}/method/Groups.get?user_id={user_id}&fields={fields}&offset={offset}&count={count}&access_token={client["token"]}').json()
