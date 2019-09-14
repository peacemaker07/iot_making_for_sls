import logging
import ssl
from urllib.error import URLError, HTTPError
from .helper import get_env
import slackweb

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Slack:

    slack_url = get_env('SLACK_NOTIFY_URL')

    @staticmethod
    def notify(slack_url, message):

        ssl._create_default_https_context = ssl._create_unverified_context
        slack = slackweb.Slack(url=slack_url)

        try:
            slack.notify(text=message, username="environment-notification", icon_emoji=":bell:")
        except HTTPError as e:
            logger.error("Request failed: %d %s", e.code, e.reason)
        except URLError as e:
            logger.error("Server connection failed: %s", e.reason)
