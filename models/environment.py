from models.dynamo import BaseDynamo


class EnvironmentDynamoDB(BaseDynamo):

    table_name = 'environment-from-soracom'

