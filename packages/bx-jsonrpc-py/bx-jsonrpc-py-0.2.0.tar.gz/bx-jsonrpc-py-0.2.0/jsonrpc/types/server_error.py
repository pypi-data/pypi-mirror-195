import enum
import json
from typing import Optional, Any, Dict


class RpcErrorCode(enum.Enum):
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603

    def message(self) -> str:
        return message_map[self]


message_map = {
    RpcErrorCode.PARSE_ERROR: "Parse error",
    RpcErrorCode.INVALID_REQUEST: "Invalid request",
    RpcErrorCode.METHOD_NOT_FOUND: "Invalid method",
    RpcErrorCode.INVALID_PARAMS: "Invalid params",
    RpcErrorCode.INTERNAL_ERROR: "Internal error",
}


class RpcError(Exception):
    def __init__(
        self,
        code: RpcErrorCode,
        request_id: Optional[str],
        data: Optional[Any],
        *,
        message: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.code = code
        if message:
            self.message = message
        else:
            self.message = code.message()

        self.data = data
        self.id = request_id

    def __str__(self):
        return (
            f"RpcError<code: {self.code}, message: {self.message}, data:"
            f" {self.data}>"
        )

    def to_json(self) -> Dict[str, Any]:
        fields = {
            "code": self.code.value,
            "message": self.message,
        }
        if self.data is not None:
            fields["data"] = self.data
        return fields

    def to_jsons(self, encoder=json.dumps) -> str:
        return encoder(self.to_json())

    @classmethod
    def from_json(cls, payload: Dict[str, Any]) -> "RpcError":
        return cls(
            RpcErrorCode(payload["code"]),
            None,
            payload.get("data"),
            message=payload.get("message"),
        )

    @classmethod
    def from_jsons(cls, payload: str, decoder=json.loads) -> "RpcError":
        return cls.from_json(decoder(payload))


class RpcParseError(RpcError):
    def __init__(
        self, request_id: Optional[str] = None, data: Optional[Any] = None
    ) -> None:
        super().__init__(RpcErrorCode.PARSE_ERROR, request_id, data)


class RpcInvalidRequest(RpcError):
    def __init__(
        self, request_id: Optional[str], data: Optional[Any] = None
    ) -> None:
        super().__init__(RpcErrorCode.INVALID_REQUEST, request_id, data)


class RpcMethodNotFound(RpcError):
    def __init__(
        self, request_id: Optional[str], data: Optional[Any] = None
    ) -> None:
        super().__init__(RpcErrorCode.METHOD_NOT_FOUND, request_id, data)


class RpcInvalidParams(RpcError):
    def __init__(
        self, request_id: Optional[str], data: Optional[Any] = None
    ) -> None:
        super().__init__(RpcErrorCode.INVALID_PARAMS, request_id, data)


class RpcInternalError(RpcError):
    def __init__(
        self, request_id: Optional[str], data: Optional[Any] = None
    ) -> None:
        super().__init__(RpcErrorCode.INTERNAL_ERROR, request_id, data)
