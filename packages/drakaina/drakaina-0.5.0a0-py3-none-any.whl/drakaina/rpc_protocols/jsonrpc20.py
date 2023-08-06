from typing import Any
from typing import Optional
from typing import Union

from drakaina.exceptions import AuthenticationFailedError
from drakaina.exceptions import BadRequestError
from drakaina.exceptions import DeserializationError
from drakaina.exceptions import ForbiddenError
from drakaina.exceptions import InternalServerError
from drakaina.exceptions import InvalidPermissionsError
from drakaina.exceptions import InvalidTokenError
from drakaina.exceptions import NotFoundError
from drakaina.exceptions import RPCError
from drakaina.exceptions import SerializationError
from drakaina.registries import RPCRegistry
from drakaina.rpc_protocols.base import BaseRPCProtocol
from drakaina.serializers import BaseSerializer
from drakaina.serializers import JsonSerializer
from drakaina.typing_ import JSONRPCRequest
from drakaina.typing_ import JSONRPCRequestObject
from drakaina.typing_ import JSONRPCResponse
from drakaina.typing_ import JSONRPCResponseObject


class JsonRPCError(RPCError):
    """JSON-RPC Common error

    Reserved for implementation-defined server-errors.
    Codes -32000 to -32099.

    """

    code: int = -32000
    default_message: str = "Server error"
    id: Union[int, str] = None
    data: Any = None

    def __init__(
        self,
        *args,
        message: str = None,
        id: Union[int, str] = None,
        data: Optional[Any] = None,
    ):
        super().__init__(*args)

        self.id = id
        if message:
            self.message = message

        if self.message and data:
            self.data = {"text": self.message.strip(), "details": data}
        elif self.message:
            self.data = self.message.strip()
        elif data:
            self.data = data

    def __str__(self) -> str:
        return f"{self.__class__.__name__} ({self.code} {self.default_message})"

    def as_dict(self) -> JSONRPCResponseObject:
        error = dict(
            jsonrpc="2.0",
            error={"code": self.code, "message": self.default_message},
            id=self.id,
        )

        if self.data:
            error["error"]["data"] = self.data

        return error


class InvalidRequestError(JsonRPCError):
    """Invalid Request

    The JSON sent is not a valid Request object.

    """

    code = -32600
    default_message = "Invalid Request"


class MethodNotFoundError(JsonRPCError):
    """Method not found

    The method does not exist / is not available.

    """

    code = -32601
    default_message = "Method not found"


class InvalidParamsError(JsonRPCError):
    """Invalid params

    Invalid method parameter(s).

    """

    code = -32602
    default_message = "Invalid params"


class InternalError(JsonRPCError):
    """Internal error

    Internal JSON-RPC error.

    """

    code = -32603
    default_message = "Internal error"


class ParseError(JsonRPCError):
    """Parse error

    Invalid JSON was received by the server.
    An error occurred on the server while parsing the JSON text.

    """

    code = -32700
    default_message = "Parse error"


# Implementation of Drakaina errors


class AuthenticationFailedJRPCError(JsonRPCError):
    """Authentication failed"""

    code = -32010
    default_message = "Authentication failed"


class InvalidTokenJRPCError(AuthenticationFailedJRPCError):
    """Invalid token error"""

    code = -32011
    default_message = "Invalid token error"


class ForbiddenJRPCError(AuthenticationFailedJRPCError):
    """Forbidden error"""

    code = -32012
    default_message = "Forbidden"


class InvalidPermissionsJRPCError(ForbiddenJRPCError):
    """Invalid permissions error"""

    code = -32013
    default_message = "Invalid permissions error"


class JsonRPCv2(BaseRPCProtocol):
    """JSON-RPC 2.0 implementation.

    :param registry:
        Registry of remote procedures.
        Default: `drakaina.registries.rpc_registry` (generic module instance)
    :type registry: RPCRegistry
    :param serializer:
        Serializer object. Default: `JsonSerializer` (stdlib.json)
    :type serializer: BaseSerializer

    """

    def __init__(
        self,
        registry: Optional[RPCRegistry] = None,
        serializer: Optional[BaseSerializer] = None,
    ):
        super().__init__(registry=registry)
        self.serializer = serializer or JsonSerializer()

        self._errors_map = {
            Exception: JsonRPCError,
            RPCError: JsonRPCError,
            BadRequestError: InvalidRequestError,
            NotFoundError: MethodNotFoundError,
            # None: InvalidParamsError,
            InternalServerError: InternalError,
            SerializationError: InternalError,
            DeserializationError: ParseError,
            AuthenticationFailedError: AuthenticationFailedJRPCError,
            InvalidTokenError: InvalidTokenJRPCError,
            ForbiddenError: ForbiddenJRPCError,
            InvalidPermissionsError: InvalidPermissionsJRPCError,
        }

    def handle(
        self,
        rpc_request: JSONRPCRequest,
        request: Optional[Any] = None,
    ) -> Optional[JSONRPCResponse]:
        """Handles a procedure call or batch of procedure call

        :param rpc_request:
            RPC request in protocol format.
        :type rpc_request: JSONRPCRequest
        :param request:
            Optional parameter that can be passed as an
            argument to the procedure.
        :type request: Any
        :return:
            Returns the result in protocol format.
        :rtype: JSONRPCResponse

        """
        # Check bad request
        if not (isinstance(rpc_request, (dict, list)) and len(rpc_request) > 0):
            return InvalidRequestError().as_dict()

        # Handle batch request
        if isinstance(rpc_request, list):
            batch_result = []
            for request_object in rpc_request:
                result = self.execute(request_object, request=request)
                if result is not None:
                    batch_result.append(result)
            if len(batch_result) == 0:
                return None
            return batch_result

        # Handle single request
        return self.execute(rpc_request, request=request)

    def execute(
        self,
        procedure_call: JSONRPCRequestObject,
        request: Optional[Any] = None,
    ) -> Optional[JSONRPCResponseObject]:
        """Execute a remote procedure call.

        :param procedure_call:
            RPC request object in protocol format.
        :type procedure_call: JSONRPCRequestObject
        :param request:
            Optional parameter that can be passed as an
            argument to the procedure. By default, None will be passed.
        :type request: Any
        :return:
            Returns a result object in protocol format.
        :rtype: JSONRPCResponseObject

        """
        if not isinstance(procedure_call, dict):
            return InvalidRequestError().as_dict()
        method: str = procedure_call.get("method")
        params: Optional[Union[list, dict]] = procedure_call.get("params")
        request_id: Optional[Union[int, str]] = procedure_call.get("id")

        # Validate protocol
        if (
            procedure_call.get("jsonrpc") != "2.0"
            or not isinstance(method, str)
            or not (params is None or isinstance(params, (list, dict)))
            or not (request_id is None or isinstance(request_id, (int, str)))
        ):
            return InvalidRequestError(id=request_id).as_dict()

        # Getting procedure
        procedure = self.registry[method]
        if procedure is None:
            # todo: may be add optional parameter for manage it behavior
            if request_id is None:
                return None
            return MethodNotFoundError(id=request_id).as_dict()

        # Prepare parameters
        # todo: validate parameters for InvalidParamsError
        # if self.is_class:
        #     inspect.signature(self.func.__init__).bind(None, *args, **kwargs)
        # else:
        #     inspect.signature(self.func).bind(*args, **kwargs)
        # if params is constants.NOTHING:
        #     return (), {}
        # if isinstance(params, constants.JSON_PRIMITIVE_TYPES):
        #     return (params,), {}
        # if isinstance(params, typing.Sequence):
        #     return params, {}
        # if isinstance(params, typing.Mapping):
        #     return (), params
        # raise errors.InvalidParams('Params have unsupported data types.')
        args, kwargs = (), {}
        if params is not None:
            if isinstance(params, list):
                args = (request, *params)
            elif isinstance(params, dict):
                kwargs = dict(request=request, **params)
        else:
            kwargs = dict(request=request)

        # Execute RPC method
        try:
            # todo: what if method is coroutine? use asgi_ref.async_to_sync
            result = procedure(*args, **kwargs)
        except JsonRPCError as err:
            err.id = request_id
            return err.as_dict()
        except Exception as err:
            return InternalError(message=str(err), id=request_id).as_dict()

        if request_id is None:
            return None

        return dict(jsonrpc="2.0", result=result, id=request_id)

    @property
    def default_error(self):
        return InternalError

    def smd_scheme(self):
        """
        todo: check SMD scheme with specification
        https://www.simple-is-better.org/json-rpc/jsonrpc20-smd.html
        https://www.simple-is-better.org/json-rpc/jsonrpc20-schema-service-descriptor.html
        https://dojotoolkit.org/reference-guide/1.10/dojox/rpc/smd.html
        https://github.com/semrush/smdbox
        """
        raise NotImplementedError
        # smd = {
        # "serviceType": "JSON-RPC", "serviceURL": self.url, "methods": []
        # }
        #
        # if self.report_methods:
        #     smd["methods"] = [
        #         {
        #             "name": key,
        #             "parameters": [
        #                 a for a in getfullargspec(value).args
        #                 if a not in RESERVED_KWARGS
        #             ],
        #         }
        #         for key, value in self._remote_procedures.items()
        #     ]
        #
        # return smd

    def openrpc_scheme(self):
        raise NotImplementedError

    def openapi_scheme(self):
        raise NotImplementedError

    # @staticmethod
    # def _valid_params(method, params):
    #     """
    #     Validates type, and number of params. Raises ``ParamsError`` when a
    #     missmatch is found.
    #     """
    #     # ``list`` (JavaScript Array) based "params"
    #     if isinstance(params, list):
    #         params_list = []
    #         for idx, defined in enumerate(method.rpc_params):
    #             try:
    #                 provided = params[idx]
    #             except IndexError:
    #                 # JSON-RPC 1.1 spec states that parameters should be
    #                 # replaced with a "nil" object, but instead let's raise an
    #                 # exception, unless the param is marked optional with "?".
    #                 if defined['optional']:
    #                     provided = None  # Set value to "nil" (None)
    #                 else:
    #                     raise InvalidParamsError(
    #                         data=u'Parameter `{0}` is required, but was '
    #                         'not provided'.format(defined['name']))
    #             if not type(provided) == JSONType(defined['type']):
    #                 if defined['optional'] and provided is None:
    #                     pass  # Optional params are allowed to be "nil"
    #                 else:
    #                     raise InvalidParamsError(
    #                         data=u'`{0}` param should be of type '
    #                         '{1}'.format(defined['name'], defined['type']))
    #             params_list.append(provided)
    #         return params_list
    #     # ``dict`` (JavaScript object) based "params"
    #     elif isinstance(params, dict):
    #         params_dict = {}
    #         for defined in method.rpc_params:
    #             name = defined['name']
    #             try:
    #                 provided = params[name]
    #             except KeyError:
    #                 if defined['optional']:
    #                     provided = None  # Set value to "nil" (None)
    #                 else:
    #                     raise InvalidParamsError(
    #                         data=u'Parameter `{0}` is required, but was '
    #                         'not provided'.format(defined['name']))
    #             if not type(provided) == JSONType(defined['type']):
    #                 if defined['optional'] and provided is None:
    #                     pass  # Optional params are allowed to be "nil"
    #                 else:
    #                     raise InvalidParamsError(
    #                         data=u'`{0}` param should be of type '
    #                         '{1}'.format(defined['name'], defined['type']))
    #             params_dict[name] = provided
    #         return params_dict
    #     else:
    #         raise InvalidParamsError(
    #             data=u'The `params` argument must be an array or object')
