from datetime import datetime
from datetime import timedelta
from datetime import UTC
from functools import lru_cache
from typing import Any
from typing import Optional
from typing import Protocol
from typing import Union
from uuid import uuid4

import jwt
from jwt import algorithms
from jwt import encode
from jwt import InvalidAlgorithmError
from jwt import InvalidTokenError
from jwt import PyJWKClient

from drakaina.contrib.jwt import jwt_config
from drakaina.contrib.jwt.errors import JWTError
from drakaina.contrib.jwt.errors import InvalidJWTTokenError
from drakaina.contrib.jwt.errors import JWTTokenHasExpired

ACCESS_KEY = "jwt-access"
REFRESH_KEY = "jwt-refresh"
USER_ID_KEY = "drakaina.user_id"
USER_KEY = "drakaina.user"


class GetUserID(Protocol):
    """Interface your callback for creating new user

    Example:

        >>> def get_user_id(form_data, request):
        >>>     user = authenticate(**form_data)
        >>>     if user is None or not user.is_active:
        >>>         raise AuthenticationFailedError(
        >>>             "No active account found with the given credentials",
        >>>         )
        >>>     if "UPDATE_LAST_LOGIN":
        >>>         update_last_login(None, self.user)
        >>>     return user.id

    Parameters:

    form_data: dict[str, str]
        Form data
    request: Any
        Request environ

    Returns:
        what

    Raise:

    AuthenticationError
        some error

    """

    def __call__(
        self,
        form_data: dict[str, str],
        request: Optional[Any] = None,
    ) -> Optional[Union[int, str]]:
        """Interface your callback for creating new user

        Example:

            >>> def get_user_id(form_data, request):
            >>>     user = authenticate(**form_data)
            >>>     if user is None or not user.is_active:
            >>>         raise AuthenticationFailedError(
            >>>             "No active account found with the given credentials",
            >>>         )
            >>>     if "UPDATE_LAST_LOGIN":
            >>>         update_last_login(None, self.user)
            >>>     return user.id

        :param form_data:
        :type form_data: dict[str, str]
        :param request:
        :type request: Any
        :returns:
        :raise AuthenticationError:
        """
        ...


class GetNewUserID(Protocol):
    def __call__(
        self,
        form_data: dict[str, str],
        request: Optional[Any] = None,
    ) -> Optional[Union[int, str]]:
        """Interface your callback for creating new user

        Example:

            >>> def get_new_user_id(form_data, request):
            >>>     # querying database to check if user already exist
            >>>     user = db.get(data.email, None)
            >>>     if user is not None:
            >>>         raise HTTPException(
            >>>             status_code=status.HTTP_400_BAD_REQUEST,
            >>>             detail="User with this email already exist",
            >>>         )
            >>>     user = {
            >>>         "email": data.email,
            >>>         "password": get_hashed_password(data.password),
            >>>         "id": str(uuid4()),
            >>>     }
            >>>     db[data.email] = user  # saving user to database
            >>>     return user.id

        :param form_data:
        :type form_data: dict[str, str]
        :param request:
        :type request: Any
        :returns:
        :raise AuthenticationFailedError:
        """
        ...


"""
For RCA algorithms

>>> private_key = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."
>>> public_key = b"-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC..."

>>> encoded = jwt.encode({"some": "payload"}, private_key, algorithm="RS256")

>>> print(encoded)
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.\\
4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg

>>> decoded = jwt.decode(encoded, public_key, algorithms=["RS256"])
{'some': 'payload'}

# If passphrase need

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

pem_bytes = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."
passphrase = b"your password"

private_key = serialization.load_pem_private_key(
    pem_bytes, password=passphrase, backend=default_backend()
)
encoded = jwt.encode({"some": "payload"}, private_key, algorithm="RS256")

"""


# region Utils


def datetime_utc_now() -> datetime:
    return datetime.now(tz=UTC)


def datetime_to_timestamp(dt: datetime) -> int:
    return int(dt.timestamp())


def datetime_from_timestamp(ts: int) -> datetime:
    return datetime.fromtimestamp(ts, tz=UTC)


def set_issuer(payload: dict[str, Any], value: str, claim: str = "iss"):
    """todo
    https://tools.ietf.org/html/rfc7519#section-4.1.1
    """
    payload[claim] = value


def set_subject(payload: dict[str, Any], value: str, claim: str = "sub"):
    """todo
    https://tools.ietf.org/html/rfc7519#section-4.1.2
    """
    payload[claim] = value


def set_audience(payload: dict[str, Any], value: str, claim: str = "aud"):
    """todo
    https://tools.ietf.org/html/rfc7519#section-4.1.3
    """
    payload[claim] = value


def set_expiration(
    payload: dict[str, Any],
    now: datetime,
    lifetime: timedelta,
    claim: str = "exp",
):
    """Updates the expiration time of a token.
    https://tools.ietf.org/html/rfc7519#section-4.1.4
    """
    payload[claim] = datetime_to_timestamp(now + lifetime)


def set_not_before(
    payload: dict[str, Any],
    now: datetime,
    timeout: timedelta,
    claim: str = "nbf",
):
    """todo
    https://tools.ietf.org/html/rfc7519#section-4.1.5
    """
    payload[claim] = datetime_to_timestamp(now + timeout)


def set_issued_at(payload: dict[str, Any], now: datetime, claim: str = "iat"):
    """Updates the time at which the token was issued.
    https://tools.ietf.org/html/rfc7519#section-4.1.6
    """
    payload[claim] = datetime_to_timestamp(now)


def set_jwt_id(
    payload: dict[str, Any],
    value: Optional[str] = None,
    claim: str = "jti",
):
    """Populates the configured jti claim of a token with a string where there
    is a negligible probability that the same string will be chosen at a
    later time.
    https://tools.ietf.org/html/rfc7519#section-4.1.7
    """
    payload[claim] = value if value else uuid4().hex


def check_expiration(
    payload: dict[str, Any],
    now: datetime,
    claim: str = "exp",
):
    """Checks whether a timestamp value in the given claim has passed (since
    the given datetime value in `current_time`). Raises a TokenError with
    a user-facing error message if so.
    """
    try:
        expiration_value = payload[claim]
    except KeyError:
        raise InvalidJWTTokenError(f"Token has no `{claim}` claim")

    expiration = datetime_from_timestamp(expiration_value)
    if now >= expiration:
        raise JWTTokenHasExpired(f"Token `{claim}` claim has expired")


def check_not_before(
    payload: dict[str, Any],
    now: datetime,
    claim: str = "nbf",
):
    """todo"""
    try:
        not_before_value = payload[claim]
    except KeyError:
        raise InvalidJWTTokenError(f"Token has no `{claim}` claim")

    not_before_value = datetime_from_timestamp(not_before_value)
    if now < not_before_value:
        raise InvalidJWTTokenError(f"Token `{claim}` claim not reached")


@lru_cache
def _validate_algorithm(algorithm):
    """
    Ensure that the nominated algorithm is recognized, and that cryptography
    is installed for those algorithms that require it
    """
    if algorithm not in jwt_config.SUPPORTED_ALGORITHMS:
        raise JWTError(f"Unrecognized algorithm type '{algorithm}'")

    if (
        algorithm in algorithms.requires_cryptography
        and not algorithms.has_crypto
    ):
        raise ModuleNotFoundError(
            f"To use `{algorithm}` you must install the `cryptography` package."
        )


def get_verifying_key(token):
    if jwt_config.ALGORITHM.startswith("HS"):
        return jwt_config.SIGNING_KEY

    if jwt_config.JWK_URL:
        jwks_client = PyJWKClient(jwt_config.JWK_URL)
        return jwks_client.get_signing_key_from_jwt(token).key

    return jwt_config.VERIFYING_KEY


def decode_jwt_token(token, verify=True):
    """Performs a validation of the given token and returns its payload
    dictionary.
    Raises a `TokenBackendError` if the token is malformed, if its
    signature check fails, or if its `exp` claim indicates it has expired.
    """
    try:
        payload = jwt.decode(
            token,
            get_verifying_key(token),
            algorithms=[jwt_config.ALGORITHM],
            audience=None,
            issuer=None,
            leeway=None,
            options={
                "verify_aud": jwt_config.AUDIENCE is not None,
                "verify_signature": verify,
            },
        )
    except InvalidAlgorithmError as error:
        raise JWTError("Invalid algorithm specified") from error
    except InvalidTokenError:
        raise InvalidJWTTokenError("Token is invalid or expired")

    return payload


# endregion Utils


# region Getting tokens


def get_token(
    payload: dict[str, str],
    lifetime: timedelta,
    token_type: Optional[str] = None,
) -> str:
    """todo
    Returns an encoded token for the given payload dictionary.
    """

    """
    >>> encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")

    >>> print(encoded_jwt)
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.\\
    4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg

    >>> jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
    {'some': 'payload'}

    """
    _validate_algorithm(jwt_config.ALGORITHM)

    now = datetime_utc_now()

    signing_key = jwt_config.SECRET_KEY
    if token_type:
        payload.update({"TOKEN_TYPE_CLAIM": token_type})
        if token_type == "refresh":
            signing_key = jwt_config.JWT_REFRESH_SECRET_KEY

    set_issued_at(payload, now)
    set_expiration(payload, now, lifetime)

    set_jwt_id(payload)

    if (
        jwt_config.AUDIENCE is not None
        and jwt_config.AUDIENCE_CLAIM not in payload
    ):
        set_audience(payload, jwt_config.AUDIENCE, jwt_config.AUDIENCE_CLAIM)

    if jwt_config.ISSUER is not None and jwt_config.ISSUER_CLAIM not in payload:
        set_issuer(payload, jwt_config.ISSUER, jwt_config.ISSUER_CLAIM)

    token = encode(
        payload,
        signing_key,
        jwt_config.ALGORITHM,
    )
    if isinstance(token, bytes):
        # For PyJWT <= 1.7.1
        return token.decode("utf-8")
    # For PyJWT >= 2.0.0
    return token


def get_access_token(payload: dict[str, Any], algorithm: str = "HS256") -> str:
    """todo"""
    payload = payload.copy()
    lifetime = timedelta(minutes=15)  # ACCESS_TOKEN_LIFETIME"

    no_copy = (
        "TOKEN_TYPE_CLAIM",
        "exp",
        # Both of these claims are included even though they may be the same.
        # It seems possible that a third party token might have a custom or
        # namespaced JTI claim as well as a default "jti" claim.  In that case,
        # we wouldn't want to copy either one.
        "JTI_CLAIM",
        "jti",
    )
    for claim, value in payload.items():
        if claim in no_copy:
            payload.pop(claim)

    return get_token(
        payload,
        token_type="access",
        lifetime=lifetime,
        algorithm=algorithm,
    )


def get_refresh_token(payload: dict[str, Any], algorithm: str = "HS256") -> str:
    """todo"""
    payload = payload.copy()
    lifetime = timedelta(minutes=15)  # "REFRESH_TOKEN_LIFETIME"

    return get_token(
        payload,
        token_type="refresh",
        lifetime=lifetime,
        algorithm=algorithm,
    )


def get_tokens_for(user_id: Union[int, str]) -> dict[str, str]:
    """todo
    Returns an authorization token for the given user that will be provided
    after authenticating the user's credentials.
    """
    if not isinstance(user_id, int):
        user_id = str(user_id)

    access = get_access_token({"USER_ID_CLAIM": user_id})
    refresh = get_refresh_token({"USER_ID_CLAIM": user_id})

    return {"refresh": refresh, "access": access}


# old function name `get_tokens_by`
def refresh_tokens(
    refresh_token: str,
    verify: bool = True,
    rotate_refresh: bool = False,
) -> str:
    """todo"""
    # Decode token
    payload = decode_jwt_token(refresh_token, "refresh", verify=verify)
    # raise InvalidTokenError("Token is invalid or expired")

    if verify:
        verify_refresh_token(payload)

    result = {"access": get_access_token(payload)}
    if rotate_refresh:
        result["refresh"] = get_refresh_token(payload)

    return result


# endregion Getting tokens


def verify_jwt_token(token: str):
    """todo

    :param token: Token for verification
    :except JwtTokenError: raised when the token is not valid
    """
    _validate_algorithm()

    # Decode token
    try:
        payload = decode_jwt_token(token, verify=True)
    except JWTError:
        raise InvalidTokenError("Token is invalid or expired")

    # todo: need implement blacklist? (by jti)

    verify_payload(payload, None, verify_expiration=True)


def verify_payload(
    payload: dict[str, Any],
    token_type: str,
    verify_expiration: bool = True,
):
    """
    Performs additional validation steps which were not performed when this
    token was decoded.  This method is part of the "public" API to indicate
    the intention that it may be overridden in subclasses.
    """
    now = datetime_utc_now()

    if verify_expiration:
        check_expiration(payload, now)

    # Ensure token id is present
    if jwt_config.JTI_CLAIM is not None and jwt_config.JTI_CLAIM not in payload:
        raise JWTError("Token has no id")

    # Ensures that the token type claim is present and has the correct value.
    if "TOKEN_TYPE_CLAIM" != None:
        try:
            payload["TOKEN_TYPE_CLAIM"]
        except KeyError:
            raise JWTError("Token has no type")

        if token_type != payload["TOKEN_TYPE_CLAIM"]:
            raise JWTError("Token has wrong type")


def verify_access_token(payload: dict[str, Any]):
    verify_payload(payload, "access")


def verify_refresh_token(payload: dict[str, Any]):
    verify_payload(payload, "refresh")
