from http.cookies import SimpleCookie
from typing import Any, Dict

from chattr_auth.chattr_jwt import constants as chattr_auth_constants


def request_headers_has_auth_type(request_headers: Dict[str, Any], auth_type: chattr_auth_constants.AuthTypes) -> bool:
    raw_cookie_value = request_headers.get('Cookie', '')
    cookie: SimpleCookie = SimpleCookie(raw_cookie_value)
    cookies = {k: v.value for k, v in cookie.items()}

    auth_types_in_request = cookies.get(chattr_auth_constants.X_AUTH_TYPE, '') + request_headers.get(
        chattr_auth_constants.X_AUTH_TYPE, ''
    )

    return auth_type.value in auth_types_in_request.upper()
