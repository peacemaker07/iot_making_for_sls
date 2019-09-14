import requests
from .helper import get_env


class LineNotify:

    @classmethod
    def notify(cls, message):

        payload = {'message': message}
        res = cls._requests(payload)

        return res

    @classmethod
    def _requests(cls, payload):

        url = 'https://notify-api.line.me/api/notify'
        access_token = get_env('LINE_NOTIFY_ACCESS_TOKEN')

        headers = {'authorization': 'Bearer {}'.format(access_token)}
        res = requests.post(url, headers=headers, params=payload)

        return res
