from models.iot_device import IoTDeviceDynamoDB


def scan_iot_device():

    dynamodb = IoTDeviceDynamoDB()
    return dynamodb.get_items_by_scan()
