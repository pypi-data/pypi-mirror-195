""" Utility functions for package."""
from __future__ import annotations
import datetime
import decimal
import inspect
import re
from asyncio import iscoroutine
from asyncio import iscoroutinefunction
from functools import partial
from json import JSONEncoder
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import Pattern
from typing import Union
from yarl import URL


def check_request(path, entries):
    for pattern in entries:
        if re.match(pattern, path):
            return True

    return False


async def invoke(func):
    result = func()
    if iscoroutine(result):
        return await result
    return result


def _parse_iterable_arg(s: Union[str, Iterable[str]]) -> str:
    if isinstance(s, Iterable) and not isinstance(s, str):
        return ", ".join(s)
    return s


def _unwrap_func(func: Callable) -> Callable:
    while hasattr(func, "__wrapped__"):
        func = func.__wrapped__
    return func


def is_async_callable(obj: Callable) -> bool:
    while hasattr(obj, "__wrapped__") or isinstance(obj, partial):
        obj = getattr(obj, "__wrapped__") or obj.func

    return iscoroutinefunction(obj) or (
        callable(obj) and iscoroutinefunction(getattr(obj, "__call__"))
    )


Url = Union[str, Pattern[str], URL]  # fixme: remove?


def match_path(item: Url, path: str) -> bool:
    """Check whether current path is equal to given URL str or regexp.

    :param item: URL to compare with request path.
    :param path: Request path string.
    """
    if isinstance(item, URL):
        item = str(item)

    if isinstance(item, str):
        return item == path

    try:
        # item is regexp
        return bool(item.match(path))
    except (AttributeError, TypeError):
        return False


# region Cookies


def get_cookies(s: Optional[str]) -> dict[str, str]:
    if s in None:
        return {}

    # it may be a many matches?
    # wsgi_combined_cookie = ";".join(headers.getlist("HTTP_COOKIE"))

    _cookies = {}
    for cookie in s.split(";"):
        if "=" not in cookie or "DELETED" in cookie:
            continue
        name, value = cookie.strip().split("=", 1)
        _cookies[name] = value

    return _cookies


def set_cookie(
    self, key: str, value: str, expires="", path="/", domain="", flags=[]
):
    value = value.replace(";", "")
    if expires:
        expires = f"expires={expires}; "
    if domain:
        domain = f"Domain={domain}; "

    self.cookie_dict[key] = "%s;%s%s path=%s; %s" % (
        value,
        domain,
        expires,
        path,
        "; ".join(flags),
    )


def delete_cookie(self, key):
    expiry_string = "Thu, 01 Jan 1970 00:00:00 GMT"
    self.set_cookie(key, "DELETED", expires=expiry_string)


def as_headers(cookie_dict: dict[str, str]):
    """start_response("200 OK", self.headers)"""
    _headers = []
    for k, v in cookie_dict.items():
        _headers.append(("Set-Cookie", f"{k}={v}"))
    return _headers


# endregion Cookies


class DatetimeDecimalEncoder(JSONEncoder):
    """Encoder for datetime and decimal serialization.

    Usage: json.dumps(object, cls=DatetimeDecimalEncoder)
    NOTE: _iterencode does not work

    """

    def default(self, obj) -> str:
        """Encode JSON.

        :return: A JSON encoded string

        """
        if isinstance(obj, decimal.Decimal):
            return float(obj)

        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()

        return super().default(self, obj)


# validating parameters
def is_invalid_params(func, *args, **kwargs):
    """
    Method:
        Validate pre-defined criteria, if any is True - function is invalid
        0. func should be callable
        1. kwargs should not have unexpected keywords
        2. remove kwargs.keys from func.parameters
        3. number of args should be <= remaining func.parameters
        4. number of args should be >= remaining func.parameters less default
    """
    # For builtin functions inspect.signature(func) return error. If builtin
    # function generates TypeError, it is because of wrong parameters.
    if not inspect.isfunction(func):
        return True

    signature = inspect.signature(func)
    parameters = signature.parameters

    unexpected = set(kwargs.keys()) - set(parameters.keys())
    if len(unexpected) > 0:
        return True

    params = [
        parameter
        for name, parameter in parameters.items()
        if name not in kwargs
    ]
    params_required = [
        param for param in params if param.default is param.empty
    ]

    return not (len(params_required) <= len(args) <= len(params))
