import json
from boto3.dynamodb.conditions import Key
from models.environment import EnvironmentDynamoDB
from .iot_device import scan_iot_device


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


def get_range_environment_data(imsi, unix_time_from, unix_time_to):

    query_from = unix_time_from
    query_to = unix_time_to

    dynamodb = EnvironmentDynamoDB()
    query_count = 0
    all_item = []
    while True:
        query = Key('imsi').eq(imsi) & Key('timestamp').between(query_from, query_to)

        try:
            items, last_evaluated_key = dynamodb.get_items_by_query(query=query)
            if not items:
                break
            all_item.extend(items)
        except:
            all_item = []
            break

        if query_count > 10:
            # 無限ループ防止
            break

        if not last_evaluated_key:
            break
        query_from = last_evaluated_key.get('timestamp')
        if not query_from:
            break

        query_from += 1  # 取得した最後のタイムスタンプ+1から再取得する
        query_count += 1

    return all_item
