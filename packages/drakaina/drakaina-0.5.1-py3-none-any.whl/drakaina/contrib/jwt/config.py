from typing import Callable
from typing import Optional


class JWTConfig:
    SUPPORTED_ALGORITHMS = (
        "HS256",
        "HS384",
        "HS512",
        # "RS256",
        # "RS384",
        # "RS512",
    )
    ALGORITHM: str = "HS256"

    ENV_JWT_PAYLOAD = "drakaina.jwt.payload"
    ENV_JWT_TOKEN = "drakaina.jwt.token"

    ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

    JWT_USER_FIELD = "user_id"
    JWT_PERMISSIONS_FIELD = "permissions"
    # should be kept secret
    # :param secret_key: Private or Public key
    SECRET_KEY: str = None
    # refresh token with personal secret phrase
    REFRESH_SECRET_KEY: str = None

    # todo ?
    PUBLIC_KEY: str
    PRIVATE_KEY: str
    SIGNING_KEY: str
    VERIFYING_KEY: str

    CREDENTIALS_REQUIRED: bool = True

    PREFIX = "Bearer"
    AUDIENCE: Optional[str] = None
    AUDIENCE_CLAIM: str = "aud"
    ISSUER: Optional[str] = None
    ISSUER_CLAIM: str = "iss"

    def __init__(self):
        # todo: move?
        if not (self.SECRET_KEY and isinstance(self.SECRET_KEY, str)):
            raise RuntimeError(
                "Secret string or private/public key should be provided "
                "for correct work",
            )

        # todo: move?
        _validate_algorithm(self.ALGORITHM)


jwt_config = JWTConfig()
