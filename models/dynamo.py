import boto3
import json
from boto3.dynamodb.types import TypeDeserializer

from utils.helper import DecimalEncoder, get_env

deserializer = TypeDeserializer()


class BaseDynamo:

    table_name = None

    dynamodb = None
    table = None

    def __init__(self, region_name='ap-northeast-1'):

        aws_access_key_id = get_env('HVF_ACCESS_KEY_ID')
        aws_secret_access_key = get_env('HVF_SECRET_ACCESS_KEY')

        self.dynamodb = boto3.resource(
            service_name='dynamodb',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        stage = get_env('ENV')
        table_name = f'{self.table_name}-{stage}'

        self.table = self.dynamodb.Table(table_name)

    def put_item(self, item):
        res = self.table.put_item(Item=item)
        return res

    def query(self, key_condition_expression):
        res = self.table.query(KeyConditionExpression=key_condition_expression)
        return res

    def get_items_by_query(self, query=None):

        res = self.query(query)
        items = res['Items']

        last_evaluated_key = res.get('LastEvaluatedKey')
        last_evaluated_key_str = json.dumps(last_evaluated_key, indent=4, cls=DecimalEncoder) if last_evaluated_key else None
        last_evaluated_key = json.loads(last_evaluated_key_str) if last_evaluated_key_str else None

        items = self.get_items_to_dict_list(items)

        return items, last_evaluated_key

    @staticmethod
    def get_items_to_dict_list(items):

        item_str_list = [json.dumps(item, indent=4, cls=DecimalEncoder) for item in items]
        dict_list = [json.loads(item_str) for item_str in item_str_list]

        return dict_list