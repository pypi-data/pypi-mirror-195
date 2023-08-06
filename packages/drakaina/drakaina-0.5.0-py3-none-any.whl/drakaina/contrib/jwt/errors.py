from drakaina.exceptions import RPCError


class JWTError(RPCError):
    """"""


class InvalidJWTTokenError(JWTError):
    """Invalid JWT token error"""


class InvalidJWTPermissionsError(JWTError):
    """Invalid JWT permissions error"""


class AuthenticationHeaderMissing(JWTError):
    """"""


class JWTTokenHasExpired(InvalidJWTTokenError):
    """"""
