from collections.abc import Callable
from inspect import getfullargspec
from typing import Any
from typing import Dict
from typing import Iterator
from typing import Optional
from typing import Tuple

__all__ = (
    "is_rpc_procedure",
    "RPCRegistry",
    "RPC_REGISTERED",
    "RPC_NAME",
    "RPC_PROVIDE_REQUEST",
    "RPC_META",
)

# Reserved procedure argument names
RESERVED_KWARGS = ("self", "request")

# RPC procedure fields
RPC_REGISTERED = "__rpc_procedure"
RPC_NAME = "__rpc_name"
RPC_PROVIDE_REQUEST = "__rpc_provide_request"
RPC_META = "__rpc_metadata"


def is_rpc_procedure(func: Callable) -> bool:
    return hasattr(func, RPC_REGISTERED)


class RPCRegistry:
    """Registry of remote procedures"""

    _remote_procedures: Dict[str, Callable[..., Any]]

    def __init__(self):
        self._remote_procedures = {}

    def register_procedure(
        self,
        procedure: Callable[..., Any],
        name: Optional[str] = None,
        provide_request: Optional[bool] = None,
        metadata: Optional[dict] = None,
    ):
        """Register a function as a remote procedure.

        :param procedure:
            Registered procedure.
        :type procedure: Callable
        :param name:
            Procedure name. Default as function name.
        :type name: str
        :param provide_request:
            If `True`, then the request object or context can be supplied to
            the procedure as a `request` argument.
        :type provide_request: bool
        :param metadata:
            Metadata that can be processed by middleware.
        :type metadata: dict

        """
        assert callable(procedure)

        procedure_name = procedure.__name__ if name is None else name
        self.__set_attributes(
            procedure,
            procedure_name,
            provide_request,
            metadata,
        )
        # todo: provide_request and reserved kwargs - think about it
        # doc = func.__doc__
        # def _unwrap_func(func: Callable) -> Callable:
        #     while hasattr(func, '__wrapped__'):
        #         func = func.__wrapped__
        #     return func
        # def _inspect_func(self, func) -> None:
        #     is_class = inspect.isclass(func)
        #     func = func.__init__ if is_class else _unwrap_func(func)
        #     argspec = inspect.getfullargspec(func)
        #     if self.is_class or inspect.ismethod(func):
        #         self.supported_args = tuple(argspec.args[1:])
        #     else:
        #         self.supported_args = tuple(argspec.args)
        #     self.supported_kwargs = tuple(argspec.kwonlyargs)
        #     is_coroutine = asyncio.iscoroutinefunction(func)
        procedure.__rpc_args = [
            a
            for a in getfullargspec(procedure).args
            if a not in RESERVED_KWARGS
        ]

        self._remote_procedures[procedure_name] = procedure

    def __set_attributes(
        self,
        func: Callable,
        name: str,
        provide_request: bool,
        metadata: dict = None,
    ):
        setattr(func, RPC_REGISTERED, True)
        setattr(func, RPC_NAME, name)
        setattr(func, RPC_PROVIDE_REQUEST, provide_request)
        setattr(func, "__rpc_registry", self)
        setattr(func, RPC_META, metadata or {})
        # If it's a wrapped function
        __wrapped__ = getattr(func, "__wrapped__", None)
        while __wrapped__ is not None:
            setattr(__wrapped__, RPC_REGISTERED, True)
            setattr(__wrapped__, RPC_NAME, name)
            setattr(__wrapped__, RPC_PROVIDE_REQUEST, provide_request)
            setattr(__wrapped__, "__rpc_registry", self)
            setattr(__wrapped__, RPC_META, metadata or {})
            __wrapped__ = getattr(__wrapped__, "__wrapped__", None)

    def __getitem__(self, key: str) -> Optional[Callable]:
        return self._remote_procedures.get(key)

    def __setitem__(self, key: str, value: Callable):
        self.register_procedure(procedure=value, name=key)

    def __delitem__(self, key: str):
        del self._remote_procedures[key]

    def __len__(self) -> int:
        return len(self._remote_procedures)

    def __iter__(self) -> Iterator[str]:
        yield self._remote_procedures

    def get(
        self,
        key: str,
        default: Optional[Callable] = None,
    ) -> Optional[Callable]:
        return self._remote_procedures.get(key, default)

    def items(self) -> Iterator[Tuple[str, Callable]]:
        yield self._remote_procedures.items()

    def schema(self) -> dict:
        # todo: ?
        return {
            "proc_name": (
                ("arg1", "arg2"),
                None,
            ),
            "proc_name2": (
                {
                    "arg1": {
                        "type": int,
                    },
                    "arg2": int,
                },
                int,
            ),
        }
