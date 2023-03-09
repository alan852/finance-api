import jwt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..utils import get_env, ENV


def verify(token: str) -> bool:
    config = {
        "DOMAIN": get_env(ENV.AUTH0_DOMAIN),
        "API_AUDIENCE": get_env(ENV.AUTH0_API_AUDIENCE),
        "ISSUER": get_env(ENV.AUTH0_ISSUER),
        "ALGORITHMS": get_env(ENV.AUTH0_ALGORITHMS)
    }
    jwks_url = f'https://{config["DOMAIN"]}/.well-known/jwks.json'
    jwks_client = jwt.PyJWKClient(jwks_url)
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token).key
        jwt.decode(
            jwt=token,
            key=signing_key,
            algorithms=config["ALGORITHMS"],
            audience=config["API_AUDIENCE"],
            issuer=config["ISSUER"]
        )
    except Exception:
        return False
    return True


class Auth0Bearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(Auth0Bearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(Auth0Bearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=401, detail="Unauthorised")
            if not verify(credentials.credentials):
                raise HTTPException(status_code=401, detail="Unauthorised")
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Unauthorised")
