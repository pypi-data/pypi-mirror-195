from datetime import datetime, timedelta
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional

AUTHORIZATION_HEADER = 'Authorization'


class ExtendedDataclass:
    def to_dict(self) -> dict:
        return asdict(self)  # noqa


@dataclass
class User(ExtendedDataclass):
    id: int
    roles: List[str]


@dataclass
class Brand(ExtendedDataclass):
    id: int


@dataclass
class AuthedUser(ExtendedDataclass):
    user: User
    brand: Brand
    _impersonator: str = ''

    @classmethod
    def from_dict(cls, authed_user_dict: Dict[str, dict]) -> Optional['AuthedUser']:
        if not authed_user_dict:
            return None

        claims = authed_user_dict.get('claims', {})
        return cls(
            user=User(id=claims.get('user'), roles=claims.get('roles')),
            brand=Brand(id=claims.get('brand')),
            _impersonator=authed_user_dict.get('act', {}).get('sub'),
        )

    @property
    def user_id(self) -> int:
        return self.user.id

    @property
    def brand_id(self) -> int:
        return self.brand.id

    @property
    def impersonator(self) -> str:
        return self._impersonator

    @property
    def roles(self) -> List[str]:
        return self.user.roles


@dataclass
class JwtConfig(ExtendedDataclass):
    key: str
    alg: str = 'HS256'
    iss: Optional[str] = None
    iss_fqdn: Optional[str] = None
    aud: Optional[str] = None
    aud_domain: Optional[str] = None
    verify_signature: bool = True
    verify_exp: bool = True
    verify_nbf: bool = False
    verify_iat: bool = True
    verify_aud: bool = True
    verify_iss: bool = True

    def get_validation_dict(self):
        return {attr: getattr(self, attr) for attr in self.__dict__ if attr.startswith('verify_')}


@dataclass
class JwtPayload:
    user: str = '1'
    roles: List[str] = field(default_factory=lambda: ['admin'])
    brand: str = '1'
    act: dict = field(default_factory=lambda: {'sub': 'user@chattrapp.local'})
    iss: str = 'https://auth.chattrapp.local/auth'
    aud: str = '*.chattrapp.local'
    iat: datetime = datetime.utcnow()
    exp: datetime = datetime.utcnow() + timedelta(minutes=5)

    def to_dict(self) -> dict:
        return {
            'claims': {
                'user': self.user,
                'roles': self.roles,
                'brand': self.brand,
            },
            'act': self.act,
            'iss': self.iss,
            'aud': self.aud,
            'iat': self.iat,
            'exp': self.exp,
        }
