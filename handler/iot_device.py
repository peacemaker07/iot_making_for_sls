import json
from models.iot_device import IoTDeviceDynamoDB


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


def scan_iot_device():

    dynamodb = IoTDeviceDynamoDB()
    return dynamodb.get_items_by_scan()
