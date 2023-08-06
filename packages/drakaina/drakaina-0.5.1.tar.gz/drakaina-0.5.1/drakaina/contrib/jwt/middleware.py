from __future__ import annotations
from asyncio import iscoroutinefunction
from typing import Any
from typing import Awaitable
from typing import Optional
from typing import Protocol
from typing import Union

from drakaina import ENV_IS_AUTHENTICATED
from drakaina import ENV_USER
from drakaina import ENV_USER_ID
from drakaina.contrib.jwt import jwt_config
from drakaina.contrib.jwt.errors import AuthenticationHeaderMissing
from drakaina.contrib.jwt.errors import InvalidJWTTokenError
from drakaina.contrib.jwt.utils import decode_jwt_token
from drakaina.exceptions import AuthenticationFailedError
from drakaina.exceptions import ForbiddenError
from drakaina.middlewares.base import BaseMiddleware
from drakaina.typing_ import ASGIMessage
from drakaina.typing_ import ASGIReceive
from drakaina.typing_ import ASGIScope
from drakaina.typing_ import ASGISend
from drakaina.typing_ import WSGIApplication
from drakaina.typing_ import WSGIEnvironment
from drakaina.typing_ import WSGIResponse
from drakaina.typing_ import WSGIStartResponse
from drakaina.utils import get_cookies


class TokenGetter(Protocol):
    def __call__(
        self,
        request: Union[ASGIScope, WSGIEnvironment],
    ) -> Optional[str]:
        ...


class IsRevoked(Protocol):
    def __call__(
        self,
        request: Union[ASGIScope, WSGIEnvironment],
        payload: dict[str, Any],
    ) -> bool:
        ...


class UserGetter(Protocol):
    def __call__(
        self,
        request: Union[ASGIScope, WSGIEnvironment],
        payload: dict[str, Any],
    ) -> Optional[Any]:
        ...


def token_from_auth_header(
    request: Union[ASGIScope, WSGIEnvironment],
) -> Optional[str]:
    auth_header = request.get("HTTP_AUTHORIZATION")

    if auth_header is None and jwt_config.CREDENTIALS_REQUIRED:
        raise AuthenticationHeaderMissing("`Authorization` header is required")

    try:
        parts = auth_header.strip().split(" ")
    except ValueError:
        raise AuthenticationFailedError("Invalid `Authorization` header")

    if len(parts) == 0 or parts[0] not in jwt_config.PREFIX:
        if jwt_config.CREDENTIALS_REQUIRED:
            raise InvalidJWTTokenError("Invalid authorization token")
        return None

    if len(parts) != 2:
        raise InvalidJWTTokenError(
            "The Authorization header must contain two values "
            "separated by a space",
        )

    # if not isinstance(token, bytes):
    #     token = token.encode()

    return parts[1]


def get_token_from_cookies(
    request: Union[ASGIScope, WSGIEnvironment],
) -> Optional[str]:
    # todo
    cookie_header = request.get("HTTP_COOKIE")

    if cookie_header is None and jwt_config.CREDENTIALS_REQUIRED:
        raise AuthenticationHeaderMissing("`Authorization` header is required")

    cookies = get_cookies(cookie_header)

    access_token = cookies.get(jwt_config.ACCESS_KEY)
    # refresh_token = cookies.get(jwt_config.REFRESH_KEY)
    return access_token


class JWTAuthenticationMiddleware(BaseMiddleware):
    """todo

    :param is_revoked: Callable for checking token

    """

    __slots__ = ("get_token", "is_revoked", "get_user")

    def __init__(
        self,
        app: WSGIApplication,
        get_token: Optional[TokenGetter] = None,
        is_revoked: Optional[IsRevoked] = None,
        get_user: Optional[UserGetter] = None,
        **kwargs,
    ):
        super().__init__(app, **kwargs)

        self.get_token = token_from_auth_header
        if callable(get_token):
            self.get_token = get_token

        if callable(is_revoked):
            self.is_revoked = is_revoked

        if callable(get_user):
            self.get_user = get_user

    def __wsgi_call__(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        if environ["REQUEST_METHOD"] == "OPTIONS":
            return self.app(environ, start_response)

        token = self.token_getter(environ)

        if token is not None:
            token_payload = decode_jwt_token(token, verify=True)

            # todo: what if it coroutine?
            if callable(self.is_revoked):
                if self.is_revoked(environ, token_payload):
                    raise ForbiddenError("Token is revoked")

            if callable(self.is_revoked):
                environ[ENV_USER] = self.get_user(environ, token_payload)

            environ[ENV_USER_ID] = token_payload[jwt_config.JWT_USER_FIELD]
            environ[ENV_IS_AUTHENTICATED] = True
            environ[jwt_config.ENV_JWT_PAYLOAD] = token_payload

        return self.app(environ, start_response)

    async def __asgi_call__(
        self,
        scope: ASGIScope,
        receive: ASGIReceive,
        send: ASGISend,
    ) -> Awaitable:
        ...

    def token_getter(self, environ) -> str:
        """todo

        try:
            if iscoroutinefunction(self.verify_header):
                scopes, user = await self.verify_header(conn.headers)
            else:
                scopes, user = self.verify_header(conn.headers)
        except Exception as exception:
            raise AuthenticationFailedError(exception) from None
        """
        if callable(self.get_token):
            if iscoroutinefunction(self.get_token):
                return await self.get_token(environ)
            return self.get_token(environ)
        return token_from_auth_header(environ)


# region fast api

"""
https://github.com/code-specialist/fastapi-auth-middleware
Version 2.0
"""

# FastAPI = TypeVar["fastapi.FastAPI"]
# AuthenticationBackend = TypeVar[
#     "starlette.authentication.AuthenticationBackend"
# ]
# # AuthenticationFailedError = TypeVar[
# #     "starlette.authentication.AuthenticationFailedError"
# # ]
# AuthCredentials = TypeVar["starlette.authentication.AuthCredentials"]
# BaseUser = TypeVar["starlette.authentication.BaseUser"]
# AuthenticationMiddleware = TypeVar[
#     "starlette.authentication.authentication.AuthenticationMiddleware"
# ]
# MutableHeaders = TypeVar["starlette.datastructures.MutableHeaders"]
# HTTPConnection = TypeVar["starlette.requests.HTTPConnection"]
# Request = TypeVar["starlette.requests.Request"]
# JSONResponse = TypeVar["starlette.responses.JSONResponse"]
# PlainTextResponse = TypeVar["starlette.responses.PlainTextResponse"]
#
#
# class FastAPIUser(BaseUser):
#     ...
#
#
# """
# from fastapi import FastAPI
# from fastapi_auth_middleware import OAuth2Middleware
#
#
# def get_new_token(old_token: str):
#     # TODO: implement this logic
#     return "eyJgh..."
#
#
# def get_public_key():
#     with open("key.pem") as keyfile:
#         return keyfile.readlines()
#
#
# app = FastAPI()
# # Add the middleware with a public key for your JWT signer
# app.add_middleware(OAuth2Middleware, public_key=get_public_key())
# # Add the middleware with the function that will return a new token and a public key for your JWT signer
# app.add_middleware(OAuth2Middleware, get_new_token=get_new_token, public_key=get_public_key())
#
# """
#
#
# class OAuth2Middleware:
#     def __init__(
#         self,
#         app: FastAPI,
#         public_key: str,
#         get_new_token: callable = None,
#         get_scopes: callable = None,
#         get_user: callable = None,
#         decode_token_options: dict = None,
#         issuer: str = None,
#         audience: str = None,
#         algorithms: str or List[str] = None,
#     ):
#         """Constructor if the OAuth2Middleware
#         Args:
#             app (FastAPI): FastAPI instance
#             get_new_token (callable): Optional: Function that returns a new
#                         token with an old one. Takes an access token as input
#                         argument Most likely you have a refresh token stored
#                         somewhere to renew the token. Default will not renew
#                         the token and raise a HTTP 401 instead.
#             public_key (str): Public key of your OAuth2 Service to verify the
#                         jwt's signature
#             get_scopes (callable): Optional: A method that returns a list of
#                         scopes based on a decoded_token input. Default will
#                         extract scopes from the token.
#             get_user (callable): Optional: A method that returns a user Object
#                         based on a decoded_token input. Default will create
#                         a basic user from the token.
#             decode_token_options (dict): Optional: A dictionary of decode
#                         options. Possible options are: verify_iat, verify_nbf,
#                         verify_exp, verify_iss, verify_aud. Default is
#                         {"verify_exp": True, "verify_iat": True,
#                         "verify_nbf": False, "verify_iss": False,
#                         "verify_aud": False }
#             issuer (str): The issuer of the jwt. Required if the "verify_iss"
#                         option is enabled
#             audience (str): The audience of the jwt. Required if the
#                         "verify_aud" option is enabled
#         """
#         self.app = app
#         self.backend: OAuth2Backend = OAuth2Backend(
#             public_key=public_key,
#             get_scopes=get_scopes,
#             get_user=get_user,
#             decode_token_options=decode_token_options,
#             issuer=issuer,
#             audience=audience,
#             algorithms=algorithms,
#         )
#         self.get_new_token = get_new_token
#
#     async def __call__(
#         self, scope: ASGIScope, receive: ASGIReceive, send: ASGISend
#     ):
#         # Filter for relevant requests
#         if scope["type"] not in ["http", "websocket"]:
#             return await self.app(scope, receive, send)
#
#         connection = HTTPConnection(scope)  # Scoped connection
#
#         try:  # to Authenticate
#             scope["auth"], scope["user"] = await self.backend.authenticate(
#                 connection
#             )  # Authentication
#             await self.app(scope, receive, send)  # Token is valid
#         except AuthenticationHeaderMissing:
#             # Request has no 'Authorization' HTTP Header
#             response = PlainTextResponse(
#                 "Your request is missing an 'Authorization' HTTP header",
#                 status_code=401,
#             )
#             await response(scope, receive, send)
#             return  # End
#         except ExpiredSignatureError:
#             # Token has expired
#             if (
#                 self.get_new_token is None
#             ):  # No renewal has been set. Raise an exception (HTTP 401) instead
#                 response = PlainTextResponse(
#                     "Your 'Authorization' HTTP header is invalid",
#                     status_code=401,
#                 )
#                 await response(scope, receive, send)
#                 return  # End
#             else:
#                 # get_new_token method is implemented
#                 old_token = connection.headers.get("Authorization")
#                 new_token = self.get_new_token(old_token)  # Get a new token
#
#                 async def send_with_new_access_token(
#                     message: ASGIMessage,
#                 ) -> None:
#                     if (
#                         message["type"] == "http.response.start"
#                     ):  # Ensure this isn't called before stack is to be closed
#                         headers = MutableHeaders(scope=message)
#                         headers.append("New-Access-Token", new_token)
#                     await send(message)
#
#                 await self.app(scope, receive, send_with_new_access_token)
#
#
# class OAuth2Backend(AuthenticationBackend):
#     """OAuth2 Backend"""
#
#     def __init__(
#         self,
#         public_key: str,
#         get_scopes: callable,
#         get_user: callable,
#         issuer: str,
#         audience: str,
#         decode_token_options: dict,
#         algorithms: str or List[str],
#     ):
#         """
#         Args:
#             public_key (str): Public key of your OAuth2 Service to verify the
#                         jwt's signature
#             get_scopes (callable): Optional: A method that returns a list of
#                         scopes based on a decoded_token input. Default will
#                         extract scopes from the token.
#             get_user (callable): Optional: A method that returns a user Object
#                         based on a decoded_token input. Default will create a
#                         basic user from the token.
#             issuer (str): The issuer of the jwt. Required if the "verify_iss"
#                         option is enabled
#             audience (str): The audience of the jwt. Required if the
#                         "verify_aud" option is enabled
#             decode_token_options (dict): Optional: A dictionary of decode
#                         options. Possible options are: verify_iat, verify_nbf,
#                         verify_exp, verify_iss, verify_aud. Defaults are:
#                                          {
#                                             "verify_signature": True,# Signature
#                                             "verify_exp": True,  # Expiry
#                                             "verify_iat": True,  # Issued at
#                                             "verify_nbf": False,  # Not Before
#                                             "verify_iss": False,  # Issuer
#                                             "verify_aud": False,  # Audience
#                                             "verify_jti": False,  # JWT ID
#                                             "verify_at_hash": False,  # Audience
#                                         }
#         """
#         self.public_key = public_key
#         self.issuer = issuer
#         self.audience = audience
#         self.algorithms = algorithms
#
#         if get_scopes is None:
#             self.get_scopes = self._get_scopes  # Default fallback
#         else:
#             self.get_scopes = get_scopes
#
#         if get_user is None:
#             self.get_user = self._get_user  # Default fallback
#         else:
#             self.get_user = get_user
#
#         if decode_token_options is None:
#             self.decode_token_options = {
#                 "verify_signature": True,  # Signature
#                 "verify_exp": True,  # Expiry
#                 "verify_iat": True,  # Issued at
#                 "verify_nbf": False,  # Not Before
#                 "verify_iss": False,  # Issuer
#                 "verify_aud": False,  # Audience
#                 "verify_jti": False,  # JWT ID
#                 "verify_at_hash": False,  # Audience
#             }  # Default fallback
#         else:
#             self.decode_token_options = decode_token_options
#
#     @staticmethod
#     def _get_scopes(decoded_token: dict) -> List[str]:
#         return decoded_token["scope"].split(" ") or []
#
#     @staticmethod
#     def _get_user(decoded_token: dict) -> FastAPIUser:
#         return FastAPIUser()
#
#     async def authenticate(
#         self, conn: HTTPConnection
#     ) -> Tuple[AuthCredentials, BaseUser]:
#         if "Authorization" not in conn.headers:
#             raise AuthenticationHeaderMissing
#
#         import jwt
#
#         auth_header = conn.headers["Authorization"]
#         # Generic approach: "Bearer eyJsn..." -> "eyJsn...",
#         #                   "Access Token eyJsn..." -> "eyJsn..."
#         token = auth_header.split(" ")[-1]
#         decoded_token = jwt.decode(
#             token=token,
#             key=self.public_key,
#             options=self.decode_token_options,
#             audience=self.audience,
#             issuer=self.issuer,
#             algorithms=self.algorithms,
#         )
#
#         scopes = self.get_scopes(decoded_token)
#         user = self.get_user(decoded_token)
#
#         return AuthCredentials(scopes=scopes), user


# endregion fast api
