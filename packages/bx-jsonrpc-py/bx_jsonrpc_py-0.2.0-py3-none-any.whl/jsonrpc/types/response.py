import json
from typing import Optional, Any, Dict, Union, TypeVar, Generic

import humps

from .client_error import RpcMessageFormatException
from .case import Case
from .constants import *
from .server_error import RpcError
from .. import utils

T = TypeVar("T")


class JsonRpcResponse(Generic[T]):
    id: Optional[str]
    result: Optional[T]
    error: Optional[RpcError]
    jsonrpc_version: str = JSONRPC_VERSION

    def __init__(
        self,
        request_id: Optional[str] = None,
        result: Optional[T] = None,
        error: Optional[RpcError] = None,
    ) -> None:
        self.id = request_id
        self.result = result
        self.error = error

    def __str__(self) -> str:
        return f"JsonRpcResponse<{self.to_jsons()}>"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, JsonRpcResponse):
            return (
                self.id == o.id
                and self.result == o.result
                and self.error == o.error
                and self.jsonrpc_version == o.jsonrpc_version
            )
        else:
            return False

    def unwrap(self) -> T:
        if self.error is None:
            return self.result

        raise self.error

    def to_json(self, case: Case = Case.SNAKE) -> Dict[str, Any]:
        fields = {
            "jsonrpc": self.jsonrpc_version,
            "id": self.id,
        }
        result = self.result
        if result is not None:
            if case == Case.CAMEL and isinstance(result, dict):
                fields["result"] = humps.camelize(result)
            else:
                fields["result"] = result

        error = self.error
        if error is not None:
            fields["error"] = error.to_json()
        return fields

    def to_jsons(self, case: Case = Case.SNAKE, encoder=json.dumps) -> str:
        return encoder(self.to_json(case))

    def from_json(self, payload: Dict[str, Any]) -> "JsonRpcResponse":
        if "id" not in payload:
            raise RpcMessageFormatException(
                "response did not contain a request id"
            )

        if not ("result" not in payload) ^ ("error" not in payload):
            raise RpcMessageFormatException(
                "response contained neither (or both) result and error"
            )

        self.id = payload.get("id", None)
        self.result = payload.get("result", None)
        self.error = utils.optional_map(
            payload.get("error", None), RpcError.from_json
        )
        return self

    def from_jsons(
        self, payload: Union[bytes, str], decoder=json.loads
    ) -> "JsonRpcResponse":
        return self.from_json(decoder(payload))
