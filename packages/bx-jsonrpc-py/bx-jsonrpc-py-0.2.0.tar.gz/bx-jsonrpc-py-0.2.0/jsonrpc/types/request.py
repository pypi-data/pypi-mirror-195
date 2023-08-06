import json
from typing import Optional, Any, Dict, Union

import humps

from .client_error import RpcMessageFormatException
from .case import Case
from .constants import *


class JsonRpcRequest:
    id: Optional[str]
    method: str
    params: Any
    jsonrpc_version: str = JSONRPC_VERSION

    def __init__(
        self,
        request_id: Optional[str] = None,
        method: str = "",
        params: Any = None,
    ) -> None:
        self.id = request_id
        self.method = method
        self.params = params

    def __str__(self) -> str:
        return f"JsonRpcRequest<{self.to_json()}>"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, JsonRpcRequest):
            return (
                self.id == o.id
                and self.method == o.method
                and self.params == o.params
                and self.jsonrpc_version == o.jsonrpc_version
            )
        else:
            return False

    def to_json(self, case: Case = Case.SNAKE) -> Dict[str, Any]:
        params = self.params
        if params is not None and case == Case.CAMEL:
            params = humps.camelize(params)

        return {
            "jsonrpc": self.jsonrpc_version,
            "id": self.id,
            "method": self.method,
            "params": params,
        }

    # TODO: needs type annotation for encoder (probably module?)
    def to_jsons(self, case: Case = Case.SNAKE, encoder=json.dumps) -> str:
        json_dict = self.to_json(case)
        return encoder(json_dict)

    def from_json(self, payload: Dict[str, Any]) -> "JsonRpcRequest":
        self.id = payload.get("id", None)
        if "method" not in payload:
            raise RpcMessageFormatException("request does not contain a method")

        self.method = payload["method"]
        self.params = payload.get("params", None)
        return self

    def from_jsons(self, payload: Union[bytes, str], decoder=json.loads) -> "JsonRpcRequest":
        return self.from_json(decoder(payload))
