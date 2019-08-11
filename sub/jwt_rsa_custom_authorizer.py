import json
import requests
from jose import jwt

from utils.helper import get_env

AUTH0_DOMAIN = get_env('AUTH0_DOMAIN')
API_AUDIENCE = get_env('API_AUDIENCE')
ALGORITHMS = ["RS256"]


# Error handler
class AuthError(Exception):

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def requires_auth(event):

    token = get_token_auth_header(event)
    json_url = requests.get("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
    jwks = json.loads(json_url.text)
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }

    if not rsa_key:
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 401)

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer="https://" + AUTH0_DOMAIN + "/"
        )
    except jwt.ExpiredSignatureError:
        raise AuthError({"code": "token_expired", "description": "token is expired"}, 401)
    except jwt.JWTClaimsError:
        raise AuthError({"code": "invalid_claims",
                         "description": "incorrect claims, please check the audience and issuer"}, 401)
    except Exception:
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to parse authentication token."}, 401)

    return payload


def get_token_auth_header(params):
    """
    Obtains the Access Token from the Authorization Header
    """
    auth = get_token(params)
    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header", "description": "Authorization header must start with Bearer"}, 401)

    if len(parts) == 1:
        raise AuthError({"code": "invalid_header", "description": "Token not found"}, 401)

    if len(parts) > 2:
        raise AuthError({"code": "invalid_header", "description": "Authorization header must be Bearer token"}, 401)

    token = parts[1]
    return token


def get_token(params):
    """
    extract and return the Bearer Token from the Lambda event parameters

    :param params:
    :return:
    """

    param_type = params.get('type')
    if not param_type or param_type != 'TOKEN':
        raise AuthError({"code": "invalid_header",
                         "description": "Expected event.type parameter to have value TOKEN"},
                        401)

    authorization_token = params.get('authorizationToken')
    if not authorization_token:
        raise AuthError({"code": "authorization_header_missing", "description": "Authorization header is expected"},
                        401)

    return authorization_token


def get_policy_document(effect, resource):
    policy_document = {
        'Version': '2012-10-17',  # default version
        'Statement': [
            {
                'Action': 'execute-api:Invoke',  # default action
                'Effect': effect,
                'Resource': resource,
            }
        ]
    }

    return policy_document
