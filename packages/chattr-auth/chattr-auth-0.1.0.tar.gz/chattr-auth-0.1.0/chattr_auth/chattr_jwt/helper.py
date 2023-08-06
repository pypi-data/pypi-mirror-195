import argparse
from chattr_auth import JwtService, JwtConfig, JwtPayload


def make_jwt(service: JwtService, payload: JwtPayload) -> str:
    return service.generate_token(payload.to_dict())


if __name__ == "__main__":
    import os
    from datetime import datetime, timedelta

    parser = argparse.ArgumentParser(description='Script so useful.')
    parser.add_argument("--user", type=int, default=1)
    parser.add_argument("--roles", nargs="+", default=["admin"])
    parser.add_argument("--brand", type=int, default=1)
    parser.add_argument("--sub", type=str, default="user@chattrapp.local")
    parser.add_argument("--key", type=str, default=os.environ.get("JWT_KEY", "local"))
    parser.add_argument("--iss", type=str, default=os.environ.get("APIGATEWAY_FQDN", "auth.chattrapp.local"))
    parser.add_argument("--aud", type=str, default=os.environ.get("APPLICATION_DOMAIN", "chattrapp.local"))
    parser.add_argument("--expire_minutes", type=int, default=5)
    args = parser.parse_args()

    iss = f"https://{args.iss}/auth"
    aud = f"*.{args.aud}"

    jwt_service = JwtService(JwtConfig(alg='HS256', key=args.key, iss=iss, aud=aud))
    jwt_payload = JwtPayload(
        user=args.user,
        roles=args.roles,
        brand=args.brand,
        act={"sub": args.sub},
        iss=iss,
        aud=aud,
        exp=datetime.utcnow() + timedelta(minutes=args.expire_minutes),
    )
    jwt = make_jwt(jwt_service, jwt_payload)
    print(jwt)
