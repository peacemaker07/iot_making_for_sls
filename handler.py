import json
from sub.jwt_rsa_custom_authorizer import requires_auth, get_policy_document, AuthError
from sub.iot_device import scan_iot_device
from sub.environment import get_range_environment_data


def iot_devices(event, context):

    iot_devices = scan_iot_device()
    # imsiは除く
    for device in iot_devices:
        device.pop('imsi')

    response = {
        "statusCode": 200,
        "body": json.dumps(iot_devices)
    }

    return response


def range_environment(event, context):

    query_string = event.get('queryStringParameters')
    if not query_string:
        response = {
            "statusCode": 400,
        }
        return response

    param_from = query_string.get('from')
    param_to = query_string.get('to')
    device_id = query_string.get('device_id')
    if not param_from or not param_to or not device_id:
        response = {
            "statusCode": 400,
        }
        return response

    # device_idからimsiを取得する
    iot_devices = scan_iot_device()
    imsi = None
    for device in iot_devices:
        if device.get('device_id') == device_id:
            imsi = device.get('imsi')
            break
    if not imsi:
        response = {
            "statusCode": 400,
        }
        return response

    try:
        unix_time_from = int(param_from)
        unix_time_to = int(param_to)
    except:
        response = {
            "statusCode": 400,
        }
        return response

    range_datas = get_range_environment_data(imsi, unix_time_from, unix_time_to)
    for range_data in range_datas:
        # imsiをdevice_idとする
        range_data.pop('imsi')
        range_data.update({'device_id': device_id})
    response = {
        "statusCode": 200,
        "body": json.dumps(range_datas)
    }

    return response


def jwt_rsa_custom_authorizer(event, context):

    try:
        payload = requires_auth(event)
    except AuthError as e:
        print(e.status_code)
        print(e.error)
        return {
            'principalId': 'user',
            'policyDocument': get_policy_document('Deny', event.get('methodArn')),
            'context': {
                'message': e.error.get('code', ''),
                'status': e.status_code
            }
        }
    except Exception as e:
        return {
            'principalId': 'user',
            'policyDocument': get_policy_document('Deny', event.get('methodArn')),
        }

    return {
        'principalId': payload.get('sub'),
        'policyDocument': get_policy_document('Allow', event.get('methodArn')),
        'context': {},
    }
