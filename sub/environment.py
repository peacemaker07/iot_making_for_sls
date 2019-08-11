from boto3.dynamodb.conditions import Key
from models.environment import EnvironmentDynamoDB


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
