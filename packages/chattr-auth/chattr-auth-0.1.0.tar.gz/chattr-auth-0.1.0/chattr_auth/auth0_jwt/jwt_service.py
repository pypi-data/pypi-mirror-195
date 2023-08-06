import logging
import typing
from typing import Any, Dict
from urllib.parse import urljoin

import jwt

import chattr_auth.jwt_dataclasses as jwt_dataclasses
from chattr_auth import errors as chattr_errors
from chattr_auth.base_jwt_service import BaseJwtService

logger = logging.getLogger(__name__)


class Auth0JwtService(BaseJwtService):
    """
    Service that supports:
     - decoding Auth0 JWTs
     - helper methods to authorize requests
    """

    supported_algs = ['RS256']

    def __init__(self, jwt_validation_config: jwt_dataclasses.JwtConfig):
        super().__init__(jwt_validation_config)

    def _get_iss_from_fqdn(self, iss_fqdn: str) -> str:
        return f'https://{iss_fqdn}/'

    def _get_token_from_auth_header(self, request_headers: Dict) -> str:
        """Obtains the Access Token from the Authorization Header"""
        auth_header = self._get_auth_header(request_headers)
        if not auth_header:
            raise chattr_errors.MissingAuthHeaderError('Authorization header is expected')

        parts = auth_header.split()

        if parts[0].lower() != 'bearer':
            raise chattr_errors.InvalidAuthHeaderValueError('Authorization header must start with Bearer')
        elif len(parts) == 1:
            raise chattr_errors.InvalidAuthHeaderValueError('Token not found')
        elif len(parts) > 2:
            raise chattr_errors.InvalidAuthHeaderValueError('Authorization header must be Bearer token')

        token = parts[1]
        return token

    def authorize(self, request_headers: Dict) -> Dict[str, typing.Union[int, str]]:
        """
        authorizes JWT token, returns user_id.
        Args:
            request_headers (dict): HttpRequest object dict / Any dict.
        Returns:
            AuthedUser: JWT payload.
        """
        logger.debug(f'Authorization request for request headers: {request_headers}')

        token = self._get_token_from_auth_header(request_headers)
        return self.decode_token(token)

    def generate_token(self, payload: Any) -> str:
        raise NotImplementedError

    def decode_token(self, token: str) -> Dict[str, typing.Union[int, str]]:
        """
        decodes JWT.
        Args:
            token (str): JWT to be decoded.
        Returns:
            str: data decoded from JWT.
        """
        jwks_client = jwt.PyJWKClient(urljoin(self.jwt_validation_config.iss, '.well-known/jwks.json'))
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        return jwt.decode(
            token,
            signing_key.key,
            algorithms=[self.jwt_validation_config.alg],
            issuer=self.jwt_validation_config.iss,
            audience=self.jwt_validation_config.aud,
            options=self.jwt_validation_options,
        )
