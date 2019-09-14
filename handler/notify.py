from utils.slack import Slack
from utils.line_notify import LineNotify


def notify(event, context):

    temp = event.get('temp')

    # 温度が35度を超えたら通知
    if temp > 35:
        # slackへ通知
        Slack.notify(Slack.slack_url, f'部屋の温度が{temp}です!!!')

        # LINE Notifyへ通知
        LineNotify.notify(f'部屋の温度が{temp}です!!!')
