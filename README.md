<h1 align="center">ontology-py-sdk</h1>

<p align="center">A lightweight Python RPC Client for the ONT Blockchain</p>
<div align="center">

<a href="https://pypi.python.org/pypi/ontology-py-sdk" rel="nofollow"><img src="https://img.shields.io/pypi/v/ontology-py-sdk.svg">
</a>
<a href="https://travis-ci.org/CityOfZion/ontology-py-sdk" rel="nofollow"><img src="https://img.shields.io/travis/CityOfZion/ontology-py-sdk.svg">
</a>
<a href="https://ontology-py-sdk.readthedocs.io/en/latest/?badge=latest" rel="nofollow"><img src="https://readthedocs.org/projects/ontology-py-sdk/badge/?version=latest"></a>
<a href="https://coveralls.io/github/CityOfZion/ontology-py-sdk?branch=master" rel="nofollow"><img src="https://coveralls.io/repos/github/CityOfZion/ontology-py-sdk/badge.svg?branch=master"></a>
</div>

<ul>
<li>Free software: MIT license</li>
<li>Documentation: <a href="https://ontology-py-sdk.readthedocs.io" rel="nofollow">https://ontology-py-sdk.readthedocs.io</a>.</li>
</ul>


## Install

`pip install ontology-py-sdk`



### Basic Usage

- Get Height of blockchain
    ```
    >>> from rpc.Client import RPCClient
    >>> client = RPCClient()
    >>> blockchain_height = client.get_height()
    >>> blockchain_height
    769332
    ```
    
- Get a block
    ```
    >>> block = client.get_block(1)
    >>> block
    {
    'Transactions': [],
    'Size': 474,
    'Header': {
      'BlockRoot': '5cf9e85fe3c163e881700549bd69b34373fadf68679e9d30a7bb2d07bcd23967',
      'PrevBlockHash': 'e59e61548b7d04ae5de0a35d970a507333dbdb07760c03c87ef94f5819169fd9',
      'ConsensusPayload': '',
      'ConsensusData': 2049603899076174981,
      'Bookkeepers': ['035d60174384e923b2cba5384991689640975a6f76addae9d18381b0b53773d42d', '02b92ff1722d9f82c731589ae7e001a57e2274ae964fe4e20cee622d6c890d70dc', '02e371c6af54ca50090d92565665912300b3addde8e81492524d93e483a47f26d6', '03e764dd591f87d8b80ffd6de87663a72b8d4a5a2fa8d62fc92113df70ed89bbac'],
      'Version': 0,
      'Height': 4066,
      'Timestamp': 1531295822,
      'TransactionsRoot': '0000000000000000000000000000000000000000000000000000000000000000',
      'SigData': ['5253c97263613769a99ee67a4b360d439139b5fd4e80e0f4a8687d987750746da04a5147800a6f34d6691ec9dc7e941cc0fbbf07b1d96bff2305aa9bb08a0e2c', 'a78d0145abb3ceb6f6e58f360ca5cf585894c711297087a2f82a35bc29a47294ff2cad518e241f229879d4a0f78c7fed2295a49e50a707e69994e3d407cd9213', 'f96187405e6787a66015d141982ca817249d0ebb628e60e94916f9f901d2591aee77840e0d03d9ebb5cc0edf362c0012f1c8a270cb8d142d552b6379e04c7e45'],
      'NextBookkeeper': 'AcTX1EgGkLX77Xo41meFP1DtCeaNpZmZwc',
      'Hash': '195afe16178a76f72fe114201123671b5f74809eca6431bef50c9064fff1b465'
    },
    'Hash': '195afe16178a76f72fe114201123671b5f74809eca6431bef50c9064fff1b465'
    }
    ```
    
    
    
