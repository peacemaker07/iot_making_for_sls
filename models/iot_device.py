from models.dynamo import BaseDynamo


class IoTDeviceDynamoDB(BaseDynamo):

    table_name = 'iot-device'
