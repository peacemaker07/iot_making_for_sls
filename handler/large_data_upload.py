import json
import boto3

from utils.helper import get_env


def create_token_for_image_upload(event, context):
    """
    S3へのイメージアップロード用のアクセストークン作成とデバイスへのアクセストークンの送信処理
    デバイス側でこのアクセストークンを使用して、S3へ画像をアップロードする
    """

    # Boto3 STSクライアント
    sts = boto3.client('sts')
    # Boto3 IoTDataPlaneクライアント
    iot_data = boto3.client('iot-data')

    # Thing名
    thing_name = event.get('imsi')
    if not thing_name:
        return

    # Account ID取得
    account_id = sts.get_caller_identity().get('Account')

    # 各種環境データを取得
    s3_bucket_name_prefix = get_env('NAME_PREFIX')
    stage_env = get_env('ENV')

    # IAMのSTSからアクセストークンを取得
    token = sts.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/image_upload_s3_role",
        RoleSessionName=thing_name,
        Policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListBucket"
                    ],
                    "Resource": [
                        f"arn:aws:s3:::{s3_bucket_name_prefix}-iot-making-{stage_env}"
                    ]
                },
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Action": [
                        "s3:PutObject",
                    ],
                    "Resource": [
                        f"arn:aws:s3:::{s3_bucket_name_prefix}-iot-making-{stage_env}/{thing_name}/*"
                    ]
                },
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                    ],
                    "Resource": [
                        f"arn:aws:s3:::{s3_bucket_name_prefix}-iot-making-{stage_env}/*"
                    ]
                }
            ]
        })
    )

    # デバイスへアクセストークンをPublish
    iot_data.publish(
        topic='token/res/' + thing_name,
        qos=1,
        payload=json.dumps({
            "AccessKeyId": token['Credentials']['AccessKeyId'],
            "SecretAccessKey": token['Credentials']['SecretAccessKey'],
            "SessionToken": token['Credentials']['SessionToken']
        })
    )

