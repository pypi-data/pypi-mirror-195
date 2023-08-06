import requests as http
import json


class api:

    @staticmethod
    def auth(login='', password='', code=0, instance='openvk.co', token=''):
        if token == '':
            response = http.get(f'https://{instance}/token?username={login}&password={password}&code={code}&grant_type=password').json()
            token = str(response['access_token'])
            user_id = int(response['user_id'])
            response = {
                'instance': instance,
                'token': token,
                'id': user_id
            }
        elif token != '':
            response = {
                'instance': instance,
                'token': token
            }
        return response
