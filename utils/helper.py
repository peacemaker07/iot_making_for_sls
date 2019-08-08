import os
import json
import decimal

import yaml


class DecimalEncoder(json.JSONEncoder):
    """
    参考URL：https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html
    """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if (abs(o) % 1) > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def is_lambda():
    return True if os.getenv('LAMBDA_TASK_ROOT') and os.getenv('AWS_EXECUTION_ENV') else False


def getenv_yml(key):
    with open("serverless.env.yml", 'r') as f:
        data = yaml.load(f)
        val = data[key]
    return val


def get_env(key):

    if is_lambda():
        return os.getenv(key)
    else:
        return getenv_yml(key)
