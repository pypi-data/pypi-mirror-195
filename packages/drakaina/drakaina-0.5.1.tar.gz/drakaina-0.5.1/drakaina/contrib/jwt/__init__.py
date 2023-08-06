"""Submodule with implementations support of JWTokens

Standard: https://www.rfc-editor.org/rfc/rfc7519
"""
from asyncio import iscoroutinefunction
from functools import update_wrapper
from typing import Callable
from typing import Iterable
from typing import Protocol
from typing import TypeVar
from typing import Union

from drakaina import ENV_IS_AUTHENTICATED
from drakaina import is_rpc_procedure
from drakaina.contrib.jwt.config import jwt_config
from drakaina.contrib.jwt.errors import InvalidJWTPermissionsError
from drakaina.exceptions import ForbiddenError
from drakaina.typing_ import ASGIScope
from drakaina.typing_ import WSGIEnvironment

__all__ = (
    "jwt_config",
    "login_required",
    "check_permissions",
)
T = TypeVar("T")


# TODO: may be implement decorators for Registries for many instances


class Comparator(Protocol):
    def __call__(
        self,
        required: Iterable[str],
        provided: Union[str, Iterable[str]],
    ) -> bool:
        ...


def match_any(
    required: Iterable[str],
    provided: Union[str, Iterable[str]],
) -> bool:
    return any([scope in provided for scope in required])


def match_all(
    required: Iterable[str],
    provided: Union[str, Iterable[str]],
) -> bool:
    return set(required).issubset(set(provided))


def has_required_scope(
    required: Iterable[str],
    provided: Union[str, Iterable[str]],
) -> bool:
    """
    from starlette.authentication import requires
    @requires(["admin", "poweruser"])
    """
    for scope in required:
        if scope not in provided:
            return False
    return True


def login_required(*options, **kw_options) -> Callable:
    """Requires login decorator.

    Gives access to the procedure only to authenticated users.

    """

    def create_decorator(*_a, **_kw) -> Callable:
        """Accepts decorator parameters and returns a decorator
        to wrap the function.
        """

        def decorator(procedure: T) -> T:
            if not is_rpc_procedure(procedure):
                raise RuntimeError(
                    "Incorrect usage of decorator. Please use "
                    "the `drakaina.remote_procedure` decorator first."
                )

            def wrapped(*args, **kwargs):
                if len(args) == 0:  # noqa
                    environ: WSGIEnvironment = kwargs.get("request")
                else:
                    environ: WSGIEnvironment = args[0]

                if not environ.get(ENV_IS_AUTHENTICATED, False):
                    raise ForbiddenError("Authorization required")
                return procedure(*args, **kwargs)

            async def async_wrapped(*args, **kwargs):
                if len(args) == 0:  # noqa
                    scope: ASGIScope = kwargs.get("request")
                else:
                    scope: ASGIScope = args[0]

                if not scope.get(ENV_IS_AUTHENTICATED, False):
                    raise ForbiddenError("Authorization required")
                return await procedure(*args, **kwargs)

            if iscoroutinefunction(procedure):
                return update_wrapper(async_wrapped, procedure)
            return update_wrapper(wrapped, procedure)

        return decorator

    if len(options) == 1 and callable(options[0]):
        return create_decorator()(options[0])
    return create_decorator(*options, **kw_options)


def check_permissions(
    scopes: Union[str, Iterable[str]],
    permissions_field=jwt_config.JWT_PERMISSIONS_FIELD,
    comparator: Comparator = match_all,
) -> Callable:
    """Permission decorator.

    Gives access to the procedure only to authorized users.

    todo: reference for async code `starlette.authentication.requires`

    """
    if not callable(comparator):
        raise TypeError("comparator should be a func")

    scopes = [scopes] if isinstance(scopes, str) else list(scopes)

    def decorator(procedure: T) -> T:
        if not is_rpc_procedure(procedure):
            raise RuntimeError(
                "Incorrect usage of decorator. Please use "
                "the `drakaina.remote_procedure` decorator first."
            )

        def wrapped(*args, **kwargs):
            if len(args) == 0:  # noqa
                environ: WSGIEnvironment = kwargs.get("request")
            else:
                environ: WSGIEnvironment = args[0]

            if not environ.get(ENV_IS_AUTHENTICATED, False):
                raise ForbiddenError("Authorization required")

            payload = environ.get(jwt_config.ENV_JWT_PAYLOAD, {})
            # todo: make optional as str with delimiter
            permissions = payload.get(permissions_field, [])
            if not isinstance(permissions, Iterable):
                raise InvalidJWTPermissionsError("Invalid permissions format")

            if not comparator(scopes, permissions):
                raise ForbiddenError("Forbidden")

            return procedure(*args, **kwargs)

        async def async_wrapped(*args, **kwargs):
            if len(args) == 0:  # noqa
                scope: ASGIScope = kwargs.get("request")
            else:
                scope: ASGIScope = args[0]

            if not scope.get(ENV_IS_AUTHENTICATED, False):
                raise ForbiddenError("Authorization required")

            payload = scope.get(jwt_config.ENV_JWT_PAYLOAD, {})
            permissions = payload.get(permissions_field, [])
            if not isinstance(permissions, Iterable):
                raise InvalidJWTPermissionsError("Invalid permissions format")

            if not comparator(scopes, permissions):
                raise ForbiddenError("Forbidden")

            return await procedure(*args, **kwargs)

        if iscoroutinefunction(procedure):
            return update_wrapper(async_wrapped, procedure)
        return update_wrapper(wrapped, procedure)

    return decorator
