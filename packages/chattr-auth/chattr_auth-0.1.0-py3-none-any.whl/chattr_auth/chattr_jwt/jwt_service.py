import logging
from typing import Any, Dict, Optional

import jwt

import chattr_auth.jwt_dataclasses as jwt_dataclasses
from chattr_auth.chattr_jwt import constants as chattr_auth_constants
from chattr_auth.chattr_jwt import utils as chattr_auth_utils
from chattr_auth.base_jwt_service import BaseJwtService

logger = logging.getLogger(__name__)


class JwtService(BaseJwtService):
    """
    Service that supports:
     - (encoding, decoding) JWTs
     -  helper methods to authorize requests
    """

    def __init__(self, jwt_validation_config: jwt_dataclasses.JwtConfig):
        super().__init__(jwt_validation_config)

    def _get_iss_from_fqdn(self, iss_fqdn: str) -> str:
        return f'https://{iss_fqdn}/auth'

    def authorize(self, request_headers: Dict) -> Optional[jwt_dataclasses.AuthedUser]:
        """
        authorizes JWT token, returns AuthedUser dataclass.
        Args:
            request_headers (dict): HttpRequest object dict / Any dict.
        Returns:
            AuthedUser: authorized user info as AuthedUser dataclass.
        """
        logger.debug(f'Authorization request for request headers: {request_headers}')

        token = self._get_token_from_auth_header(request_headers)

        # prefer (access token from Authorization header) over (access token from cookies).
        # Check auth in cookies only if:
        # 1. There is no access token from Authorization Bearer header AND
        # 2. `X-Auth-Type` header is not BEARER_TOKEN_ONLY.
        if not (
            token
            or chattr_auth_utils.request_headers_has_auth_type(
                request_headers, chattr_auth_constants.AuthTypes.BEARER_TOKEN_ONLY
            )
        ):
            token = self._get_auth_cookies(request_headers)

        authed_user_dict = self.decode_token(token)

        return jwt_dataclasses.AuthedUser.from_dict(authed_user_dict)

    def generate_token(self, payload: Any) -> str:
        """
        generates JWT token from payload.
        Args:
            payload (dict): data that needs to be encoded as a token.
        Returns:
            str: generated JWT.
        """
        return jwt.encode(payload, self.jwt_validation_config.key, algorithm=self.jwt_validation_config.alg)

    def decode_token(self, token: str) -> dict:
        """
        decodes JWT.
        Args:
            token (str): JWT to be decoded.
        Returns:
            str: data decoded from JWT.
        Exceptions:
            Exceptions from `chattr_jwt/exceptions.py`
        """
        decoded_value = {}
        try:
            decoded_value = jwt.decode(
                token,
                self.jwt_validation_config.key,
                algorithms=[self.jwt_validation_config.alg],
                issuer=self.jwt_validation_config.iss,
                audience=self.jwt_validation_config.aud,
                options=self.jwt_validation_options,
            )
        except jwt.ExpiredSignatureError:
            logger.warning(f'JwtExpiredError for token')
        except (
            jwt.InvalidSignatureError,
            jwt.InvalidAudienceError,
            jwt.InvalidIssuerError,
            jwt.InvalidIssuedAtError,
        ) as e:
            logger.exception(f'JWTDecodeError')
            raise e
        except jwt.DecodeError as e:
            # temporarily reducing log level to debug, to decrease unuseful,confusing logs for clients until adaptation.
            # TO-DO: move back to info level log, when JWT starts being used
            logger.debug(f'DecodeError: {e}')

        return decoded_value
