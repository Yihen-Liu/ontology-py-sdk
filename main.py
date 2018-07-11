from rpc.Client import RPCClient, RPCEndpoint

client = RPCClient()
response = client.get_block(4066)
print (response)
