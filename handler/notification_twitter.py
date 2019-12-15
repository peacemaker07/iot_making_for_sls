import os
import json
from datetime import timezone, timedelta, datetime
from requests_oauthlib import OAuth1Session
import boto3

s3 = boto3.client('s3')


def notification_twitter(event, context):

    # print(event)

    url_media = "https://upload.twitter.com/1.1/media/upload.json"
    url_text = "https://api.twitter.com/1.1/statuses/update.json"

    # t = twitter.Api(access_token_key=os.getenv('TWITTER_ACCESS_TOKEN'),
    #                 access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    #                 consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
    #                 consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'))
    CK = os.getenv('TWITTER_CONSUMER_KEY')
    CS = os.getenv('TWITTER_CONSUMER_SECRET')
    AT = os.getenv('TWITTER_ACCESS_TOKEN')
    ATS = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    twitter = OAuth1Session(CK, CS, AT, ATS)

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    print(bucket_name)
    print(object_key)
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    print(response)
    body = response['Body'].read()

    files = {"media": body}
    req_media = twitter.post(url_media, files=files)
    if req_media.status_code != 200:
        print("MEDIA UPLOAD FAILED... %s", req_media.text)
        return

    media_id = json.loads(req_media.text)['media_id']
    # print("MEDIA ID: %d" % media_id)

    jst = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(jst)
    params = {"status": "{} testだよー".format(now.strftime("%Y/%m/%d %H:%M")), "media_ids": [media_id]}
    req_text = twitter.post(url_text, params=params)

    if req_media.status_code != 200:
        print("TEXT UPLOAD FAILED... %s", req_text.text)

    # t.PostUpdates(status=msg)
