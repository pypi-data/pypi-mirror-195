from typing import Awaitable

from drakaina.exceptions import RPCError
from drakaina.middlewares.base import BaseMiddleware
from drakaina.typing_ import ASGIReceive
from drakaina.typing_ import ASGIScope
from drakaina.typing_ import ASGISend
from drakaina.typing_ import WSGIEnvironment
from drakaina.typing_ import WSGIResponse
from drakaina.typing_ import WSGIStartResponse


class ExceptionMiddleware(BaseMiddleware):
    """"""

    def __wsgi_call__(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        try:
            return self.app(environ, start_response)
        except RPCError as error:
            return ...
        except Exception as error:
            return ...

    async def __asgi_call__(
        self,
        scope: ASGIScope,
        receive: ASGIReceive,
        send: ASGISend,
    ) -> Awaitable:
        try:
            return await self.app(scope, receive, send)
        except RPCError as error:
            return await ...
        except Exception as error:
            return await ...
