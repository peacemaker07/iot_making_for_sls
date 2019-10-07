import json
import boto3

iot_data = boto3.client('iot-data')


def is_shadow(thing_name):
    """
    Thing Shadowの有無チェック
    """
    payload_dict = get_shadow(thing_name)
    if not payload_dict:
        return False

    return True


def shadow_update(thing_name, update_payload):

    # Thing Shadowの有無を取得
    if not is_shadow(thing_name):
        return

    iot_data.update_thing_shadow(
        thingName=thing_name,
        payload=update_payload
    )


def get_shadow(thing_name):

    try:
        response = iot_data.get_thing_shadow(
            thingName=thing_name
        )
        payload = response['payload']
        payload_dict = json.loads(payload.read())
    except Exception as e:
        print(e.args)
        return {}

    return payload_dict
