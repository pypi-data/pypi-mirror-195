# drakaina

![Drakaina](content/drakaina.png "Drakaina"){width=200px height=205px}

[![image](https://img.shields.io/pypi/v/drakaina.svg)](https://pypi.python.org/pypi/drakaina)
[![image](https://img.shields.io/pypi/l/drakaina.svg)](https://pypi.python.org/pypi/drakaina)
[![image](https://img.shields.io/pypi/pyversions/drakaina.svg)](https://pypi.python.org/pypi/drakaina)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)
[![libera manifesto](https://img.shields.io/badge/libera-manifesto-lightgrey.svg)](https://liberamanifesto.com)

❗ WIP

Module for simple RPC service implementation


## Quickstart

Drakaina may be installed via `pip` and requires Python 3.7 or higher :

```shell
pip install drakaina
```

A minimal Drakaina example is:

```python
import asyncio
from drakaina import remote_procedure
from drakaina.asgi import ASGIHandler
from drakaina.wsgi import WSGIHandler


@remote_procedure
def my_method():
    return "Hello Bro! ✋️"


@remote_procedure(name="something.get")
def get_some_string():
    return "You called `something.get`."


@remote_procedure(provide_request=True)
def do_something_with_environ(request):
    return f"You called `do_something_with_environ`. Request: {request}."


@remote_procedure()
def tell_the_middleware_something():
    return "You called `tell_the_middleware_something`. It has a some extra conditions."


async def asynchronous_procedure():
    await asyncio.sleep(5)
    return "Ding-Dong 🔔!"


"""
>>> JsonRPCv2().handle({"jsonrpc": "2.0", "method": "my_method", "id": 1})
or define WSGI application
"""
app = WSGIHandler(route="/jrpc")
"""
or define ASGI application
"""
app2 = ASGIHandler(route="/ajrpc")
```

Drakaina may be ran with any WSGI-compliant server,
such as [Gunicorn](http://gunicorn.org).

```shell
gunicorn main:app
```

or ran with any ASGI-compliant server

```shell
uvicorn main:app2
```


## Features

- WSGI protocol implementation
  - Implemented CORS middleware
  - Compatible with simple middlewares for others wsgi-frameworks,
    like as [Werkzeug](https://palletsprojects.com/p/werkzeug/),
    [Flask](https://palletsprojects.com/p/flask/)


# Documentation


## Installation

```shell
pip install drakaina
```


### Optional requirements

```shell
pip install drakaina[jwt, orjson, ujson]
```


## Define remote procedures


## Middlewares


### Logging


### CORS


### JWT

Drakaina may be installed via `pip` and requires Python 3.7 or higher :

```shell
pip install drakaina[jwt]
```

A minimal Drakaina example is:

```python
from functools import partial
from drakaina import ENV_IS_AUTHENTICATED
from drakaina import ENV_USER_ID
from drakaina import remote_procedure
from drakaina.contrib.jwt import check_permissions
from drakaina.contrib.jwt import login_required
from drakaina.contrib.jwt import match_any
from drakaina.contrib.jwt.utils import encode
from drakaina.contrib.jwt.middleware import JWTAuthenticationMiddleware
from drakaina.wsgi import WSGIHandler


@login_required
@remote_procedure(provide_request=True)
def my_method(request):
    assert request[ENV_IS_AUTHENTICATED]
    return f"Hello Bro ✋! Your ID={request[ENV_USER_ID]}"


@check_permissions(
    scopes=["user_read", "app/user:admin", "username:johndoe"],
    comparison=match_any,
)
@remote_procedure
def my_method():
    return "Hello Bro! ✋️"


async def get_token(request):
    return encode(
        {"username": "johndoe", "scopes": ["username:johndoe"]},
        # sharable_secret,
    )


app = WSGIHandler(
    middlewares=[
        partial(
            JWTAuthenticationMiddleware,
            secret_phrase="_secret_",
            credentials_required=True,
            auth_scheme="Bearer",
            token_getter=get_token,
        )
    ]
)
```


### Using with Django

Create file `rpc_views.py` in your django application.
Define function and wrap it `remote_procedure` decorator:

```python
from drakaina import remote_procedure

@remote_procedure
def my_method(test: str):
    return "Hello, Django Bro! ✋"
```

Add `JsonRPCView` class to urlpatterns. The `as_view` method
must accept the `autodiscover` argument as the name of
the remote procedure files.

```python
from django.urls import path
from drakaina.contrib.django.views import JsonRPCView

urlpatterns = [
    path("api/", JsonRPCView.as_view(autodiscover="rpc_views")),
]
```


### JWT Authentication in your Django project

1. Add `jsonrpc.django` module in INSTALLED_APPS list in the `settings.py` file.
2. Define `JSONRPC_SIGNING_KEY = "Some_Secret_String"` in the `settings.py` file
3. Use `token`, `token.refresh` and `token.verify` JsonRPC methods for authentication by JWT tokens.


## ToDo

- More tests
- GZip middleware
- asgi implementation
- async middlewares implementation
- preload or server example
- implement cysimdjson serializer
- implement pickle serializer


## Credits

This module inspired by official
[auth0/express-jwt](https://github.com/auth0/express-jwt) middleware and
[express-jwt-permissions](https://github.com/MichielDeMey/express-jwt-permissions) extension.


## License

Apache License 2.0

## Artwork

"[drakaina.png](content/drakaina.png)" by Korolko Anastasia is licensed under
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="License Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/80x15.png" /></a> ([CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/)).
