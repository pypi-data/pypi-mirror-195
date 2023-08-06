# JSON-RPC Python Client

Library for interacting with JSON-RPC servers. Implements the 
[JSON-RPC 2.0 spec](https://www.jsonrpc.org/specification), as well as 
first-class support for the subscription streaming endpoints exposed by
most blockchain RPC interfaces (e.g. Ethereum, Solana) for JSON-RPC websockets
connections.

## Features
 - Websockets connection wrapper with full support for matching request IDs to responses and subscription updates to subscription IDs
 - Classes for (de)serializing JSON-RPC spec compliant message types

## Installation
```
$ pip install bx-jsonrpc-py
```

## Websockets Streaming
Many blockchains use a subscription RPC endpoint with JSON-RPC notifications
to provide real-time event streams of updates in the network. They usually look
something like this:

```
// create subscription
>> {"id": 1, "method": "subscribe", "params": ["feedName"]}
<< {"jsonrpc":"2.0","id":1,"result":"subscriptionID"}

// incoming notifications
<< {"jsonrpc":"2.0","method":"subscribe","params":{"subscription":"subscriptionID","result":"data"}}}
<< {"jsonrpc":"2.0","method":"subscribe","params":{"subscription":"subscriptionID","result":"data}}}

// cancel subscription
>> {"id": 1, "method": "unsubscribe", "params": ["subscriptionID"]}
<< {"jsonrpc":"2.0","id":1,"result":true}
```

Some examples: [go-ethereum](https://geth.ethereum.org/docs/rpc/pubsub), [solana](https://docs.solana.com/developing/clients/jsonrpc-api#subscription-websocket)

The included `jsonrpc.WsRpcConnection` class fully implements this feature.

## Usage

```python
import jsonrpc

async with jsonrpc.WsRpcConnection("ws://...") as ws:
    print(await ws.call("method", {"param": "value"}))
    
    subscription_id = await ws.subscribe(
        "feedname", {"option": "value"}
    )
    async for notification in ws.notifications_for_id(subscription_id):
        print(notification)
```

See `examples/client.py` for a working sample.

## Anticipated Future Work
 - Reconnection support for websockets to reconnect and resubscribe to former feeds

## Comments / Questions
Feel free to open up a Github issue to discuss enhancements or problems.
