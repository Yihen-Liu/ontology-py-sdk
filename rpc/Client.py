from rpc.Settings import settings as rpc_settings
import requests
import binascii


class ONTRPCException(Exception):
    pass


class RPCClient():

    id_counter = 0

    _settings = rpc_settings
    _addr_list = None

    @property
    def endpoints(self):
        return self._addr_list

    @property
    def default_endpoint(self):
        self._addr_list.sort()
        return self._addr_list[0]

    def get_height(self, id=None, endpoint=None):
        """
        Get the current height of the blockchain
        Args:
            id: (int, optional) id to use for response tracking
            endpoint: (RPCEndpoint, optional) endpoint to specify to use

        Returns:
            json object of the result or the error encountered in the RPC call
        """
        return self._call_endpoint(GET_BLOCK_COUNT, id=id, endpoint=endpoint)

    def get_best_blockhash(self, id=None, endpoint=None):
        """
        Get the hash of the highest block
        Args:
            id: (int, optional) id to use for response tracking
            endpoint: (RPCEndpoint, optional) endpoint to specify to use
        Returns:
            json object of the result or the error encountered in the RPC call
        """
        return self._call_endpoint(GET_BEST_BLOCK_HASH, id=id, endpoint=endpoint)

    def get_block(self, height_or_hash, id=None, endpoint=None):
        """
        Look up a block by the height or hash of the block.
        Args:
            height_or_hash: (int or str) either the height of the desired block or its hash in the form '1e67372c158a4cfbb17b9ad3aaae77001a4247a00318e354c62e53b56af4006f'
            id: (int, optional) id to use for response tracking
            endpoint: (RPCEndpoint, optional) endpoint to specify to use

        Returns:
            block: a json object or the ``rpc.Core.Block.Block`` object
        """
        return self._call_endpoint(GET_BLOCK, params=[height_or_hash, 1], id=id, endpoint=endpoint)

    def get_block_hash(self, height, id=None, endpoint=None):
        """
        Get hash of a block by its height
        Args:
            height: (int) height of the block to lookup
            id: (int, optional) id to use for response tracking
            endpoint: (RPCEndpoint, optional) endpoint to specify to use

        Returns:
            json object of the result or the error encountered in the RPC call
        """
        return self._call_endpoint(GET_BLOCK_HASH, params=[height], id=id, endpoint=endpoint)

    def get_contract_state(self, contract_hash, id=None, endpoint=None):
        """
        Get a contract state object by its hash
        Args:
            contract_hash: (str) the hash of the contract to lookup, for example 'd7678dd97c000be3f33e9362e673101bac4ca654'
            id: (int, optional) id to use for response tracking
            endpoint: (RPCEndpoint, optional) endpoint to specify to use
        Returns:
            json object of the result or the error encountered in the RPC call
        """
        return self._call_endpoint(GET_CONTRACT_STATE, params=[contract_hash], id=id, endpoint=endpoint)

    def get_transaction(self, tx_hash, id=None, endpoint=None):
        """
        Look up a transaction by hash.
        Args:
            tx_hash: (str) hash in the form '58c634f81fbd4ae2733d7e3930a9849021840fc19dc6af064d6f2812a333f91d'
            id: (int, optional) id to use for response tracking
            endpoint: (RPCEndpoint, optional) endpoint to specify to use

        Returns:
            json: the transaction as a json object
        """
        return self._call_endpoint(GET_RAW_TRANSACTION, params=[tx_hash, 1], id=id, endpoint=endpoint)

    def invoke_contract(self, contract_hash, params, id=None, endpoint=None):
        """
        Invokes a contract
        Args:
            contract_hash: (str) hash of the contract, for example 'd7678dd97c000be3f33e9362e673101bac4ca654'
            params: (list) a list of json ContractParameters to pass along with the invocation, example [{'type':7,'value':'symbol'},{'type':16, 'value':[]}]
            id: (int, optional) id to use for response tracking
            endpoint: (RPCEndpoint, optional) endpoint to specify to use
        Returns:
            json object of the result or the error encountered in the RPC call
        """
        return self._call_endpoint(INVOKE, params=[contract_hash, params], id=id, endpoint=endpoint)

    def send_raw_tx(self, serialized_tx, id=None, endpoint=None):
        """
        Submits a serialized tx to the network
        Args:
            serialized_tx: (str) a hexlified string of a transaction
            id: (int, optional) id to use for response tracking
            endpoint: (RPCEndpoint, optional) endpoint to specify to use
        Returns:
            bool: whether the tx was accepted or not
        """
        return self._call_endpoint(SEND_TX, params=[serialized_tx], id=id, endpoint=endpoint)

    def get_version(self, id=None, endpoint=None):
        """
        Get the current version of the endpoint.
        Note: Not all endpoints currently implement this method

        Args:
            id: (int, optional) id to use for response tracking
            endpoint: (RPCEndpoint, optional) endpoint to specify to use
        Returns:
            json object of the result or the error encountered in the RPC call
        """
        return self._call_endpoint(GET_VERSION, id=id, endpoint=endpoint)

    def __init__(self, config=None, setup=False):

        if config:
            self._settings = config

        self._build_addr()

        if setup:
            self.setup_endpoints()

    def setup_endpoints(self):
        self._build_addr()
        [endpoint.setup() for endpoint in self._addr_list]

    def _call_endpoint(self, method, params=None, id=None, endpoint=None):
        payload = self._build_payload(method, params, id)
        endpoint = self.default_endpoint if endpoint is None else endpoint
        try:
            response = requests.post(endpoint.addr, json=payload, timeout=TIMEOUT)
            response.raise_for_status()
            if response.status_code == 200:
                if 'result' in response.json():
                    return response.json()['result']
            return response.json()
        except Exception as e:
            raise ONTRPCException("Could not call method %s with endpoint: %s : %s " % (method, endpoint.addr, e))

    def _build_addr(self):
        self._addr_list = [RPCEndpoint(self, addr) for addr in self._settings.RPC_LIST]

    def _build_payload(self, method, params, id):

        id = self.id_counter if id is None else id
        self.id_counter += 1

        params = [] if params is None else params

        rpc_version = "2.0"

        return {'jsonrpc': rpc_version, 'method': method, 'params': params, 'id': id}


# methods that read data
GET_BEST_BLOCK_HASH = 'getbestblockhash'
GET_BLOCK = 'getblock'
GET_BLOCK_COUNT = 'getblockcount'
GET_BLOCK_HASH = 'getblockhash'
GET_CONTRACT_STATE = 'getcontractstate'
GET_RAW_TRANSACTION = 'getrawtransaction'
GET_VERSION = 'getversion'
# invocation related methods
INVOKE = 'invoke'
# send
SEND_TX = 'sendrawtransaction'

TIMEOUT = 10


class RPCEndpoint():
    addr = None
    height = None
    client = None
    status = None
    elapsed = None

    def __init__(self, client, address):
        self.client = client
        self.addr = address

    def setup(self):

        response = requests.post(self.addr, json={'jsonrpc': '2.0', 'method': GET_BLOCK_COUNT, 'params': [], 'id': 1})
        self.update_endpoint_details(response)

        if response.status_code == 200:
            json = response.json()
            self.height = int(json['result'])

    def update_endpoint_details(self, response):

        self.status = response.status_code
        self.elapsed = response.elapsed.microseconds

    def _compare(self, other):
        if self.status != 200:
            return -1
        elif other.status != 200:
            return 1

        if self.height == other.height:
            if self.elapsed == other.elapsed:
                return 0

            if other.elapsed > 0 and self.elapsed > 0:

                if self.elapsed > other.elapsed:
                    return 1
                else:
                    return -1
        else:

            if self.height < other.height:
                return 1
            else:
                return -1

    def __eq__(self, other):
        return self.addr == other.addr

    def __lt__(self, other):
        return self._compare(other) < 0

    def __gt__(self, other):
        return self._compare(other) > 0

    def __le__(self, other):
        return self._compare(other) <= 0

    def __ge__(self, other):
        return self._compare(other) >= 0

    def __str__(self):
        return "[%s] %s %s %s" % (self.addr, self.status, self.height, self.elapsed)
