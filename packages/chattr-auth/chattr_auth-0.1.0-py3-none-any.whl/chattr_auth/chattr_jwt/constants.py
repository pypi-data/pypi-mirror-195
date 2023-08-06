from enum import Enum

X_AUTH_TYPE = 'X-Auth-Type'


class AuthTypes(Enum):
    JWTONLY = 'JWTONLY'  # request needs to have JWT in authorization bearer header or cookie
    RETURN_UNAUTHED = 'RETURN_UNAUTHED'  # we always return a 401
    BEARER_TOKEN_ONLY = 'BEARER_TOKEN_ONLY'  # request needs to have JWT in authorization bearer header NOT cookie
