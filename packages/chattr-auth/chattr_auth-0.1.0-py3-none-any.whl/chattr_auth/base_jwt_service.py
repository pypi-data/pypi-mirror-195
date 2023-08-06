import logging
import typing
from http.cookies import SimpleCookie
from typing import Any, Dict, Optional
from abc import ABC

import chattr_auth.errors as chattr_jwt_errors
import chattr_auth.jwt_dataclasses as jwt_dataclasses

logger = logging.getLogger(__name__)


class BaseJwtService(ABC):
    """
    Service that supports:
     - (encoding, decoding) JWTs
     -  helper methods to authorize requests
    """

    supported_algs = ['HS256']
    auth_prefix = 'bearer'
    ACCESS_TOKEN_COOKIE = 'access_token_cookie'

    def __init__(self, jwt_validation_config: jwt_dataclasses.JwtConfig):
        """
        Args:
            jwt_validation_config (jwt_dataclasses.JwtValidationConfig): Config for JWT validation.
                alg (str): Cryptographical algorithm used to encode, decode JWTs.
                key (str): Key used to encode, decode JWTs.
                iss (str): Issuer of JWT (for JWT validation).
                iss_fqdn (str): Fully Qualified Domain Name of Issuer of JWT (for JWT validation).
                aud (str): Audience of JWT (for JWT validation).
                aud_domain (str): Domain of Audience of JWT (for JWT validation).
                verify_signature (bool): True
                verify_exp (bool): True
                verify_nbf (bool): False
                verify_iat (bool): True
                verify_aud (bool): True
                verify_iss (bool): True
        """

        if jwt_validation_config.alg not in self.supported_algs:
            raise chattr_jwt_errors.UnsupportedJwtAlgError(
                f'{jwt_validation_config.alg} is currently unsupported. Supported algorithms: {self.supported_algs}'
            )

        # when issuer fqdn is provided, URL to issuer for Chattr lambda is built as `https://<iss_fqdn>/auth`
        if not jwt_validation_config.iss and jwt_validation_config.iss_fqdn:
            jwt_validation_config.iss = self._get_iss_from_fqdn(jwt_validation_config.iss_fqdn)

        # when audience domain is provided, all subdomains are included as `*.<aud_domain>`
        if not jwt_validation_config.aud and jwt_validation_config.aud_domain:
            jwt_validation_config.aud = f'*.{jwt_validation_config.aud_domain}'

        self.jwt_validation_config = jwt_validation_config
        self.jwt_validation_options = jwt_validation_config.get_validation_dict()

    def _get_iss_from_fqdn(self, iss_fqdn: str) -> str:
        raise NotImplementedError

    @staticmethod
    def _get_auth_header(request_headers: Dict) -> str:
        """
        returns: Authorization header value in HttpRequest object dict / Any dict. Defaults to ''
        Args:
            request_headers (dict): HttpRequest object dict / Any dict.
        Returns:
            str: Authorization header value.
        """
        auth_header = request_headers.get(jwt_dataclasses.AUTHORIZATION_HEADER)

        if auth_header:
            return auth_header
        logger.debug(f'No Authorization header in: {request_headers}')

        return ''

    def _get_token_from_auth_header(self, request_headers: Dict) -> str:
        """
        returns: JWT in Authorization header value.
        Args:
            request_headers (dict): HttpRequest object dict / Any dict.
        Returns:
            str: JWT.
        """
        auth_header = self._get_auth_header(request_headers)

        if not auth_header.lower().startswith(self.auth_prefix):
            return ''

        return auth_header[len(self.auth_prefix) :].strip()

    def _get_auth_cookies(self, request_headers: Dict) -> str:
        """
        returns `access_token_cookie` key value of cookie (request_headers['Cookie']) if it exists, else return ''.
        Cookie value can be general cookie string like `access_token_cookie=value` or
        dict like {'access_token_cookie': 'value'}
        Args:
            request_headers (dict): HttpRequest object dict / Any dict.
        Returns:
            str: Authorization header value.
        """
        cookies: SimpleCookie = SimpleCookie()
        cookies.load(request_headers.get('Cookie', ''))

        access_token_cookie = cookies.get(self.ACCESS_TOKEN_COOKIE)
        if access_token_cookie:
            return str(access_token_cookie.value)
        logger.debug(f'No Access Token in cookies: {cookies}')

        return ''

    def authorize(self, request_headers: Dict) -> typing.Union[Optional[jwt_dataclasses.AuthedUser], Dict]:
        """
        authorizes JWT token, returns AuthedUser dataclass.
        Args:
            request_headers (dict): HttpRequest object dict / Any dict.
        Returns:
            AuthedUser: authorized user info as AuthedUser dataclass.
            or a dictionary with information from JWT
        """
        raise NotImplementedError

    def generate_token(self, payload: Any) -> str:
        """
        generates JWT token from payload.
        Args:
            payload (dict): data that needs to be encoded as a token.
        Returns:
            str: generated JWT.
        """
        raise NotImplementedError

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
        raise NotImplementedError
