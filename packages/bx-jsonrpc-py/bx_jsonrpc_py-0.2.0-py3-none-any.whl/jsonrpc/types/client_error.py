# exceptions raised by RPC client implementation in response to inconsistent behavior from server


class RpcMessageFormatException(Exception):
    pass


class RpcExecutionException(Exception):
    pass
