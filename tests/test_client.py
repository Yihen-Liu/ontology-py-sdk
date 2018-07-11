from unittest import TestCase
from rpc.Settings import SettingsHolder
from rpc.Client import RPCClient, RPCEndpoint, ONTRPCException
import binascii
import responses


class RPCClientTestCase(TestCase):

    def test_client(self):
        client = RPCClient()

        self.assertIsNotNone(client.endpoints)

        self.assertGreater(len(client.endpoints), 0)

        self.assertIsInstance(client.default_endpoint, RPCEndpoint)

        self.assertEqual(client.default_endpoint.height, None)

    def test_settings(self):
        settings = SettingsHolder()

        settings.setup_mainnet()
        client = RPCClient(config=settings)
        self.assertIsNotNone(client.endpoints)

        settings.setup_testnet()
        client = RPCClient(config=settings)
        self.assertIsNotNone(client.endpoints)

        settings.setup_privnet()
        client = RPCClient(config=settings)
        self.assertIsNotNone(client.endpoints)

    def test_client_setup(self):
        client = RPCClient(setup=True)

        self.assertIsNotNone(client.endpoints)

        self.assertGreater(len(client.endpoints), 0)

        self.assertIsInstance(client.default_endpoint, RPCEndpoint)

        self.assertIsNotNone(client.default_endpoint.height)

        self.assertEqual(client.default_endpoint.status, 200)

    def test_call_endpoint_exception(self):
        settings = SettingsHolder()

        settings.setup_privnet()
        client = RPCClient(config=settings)

        # Assumes no privnet is running (which always holds true on Travis-CI)
        with self.assertRaises(NEORPCException) as context:
            client.get_height()
        self.assertTrue("Could not call method" in str(context.exception))

    @responses.activate
    def test_call_endpoint_status_moved(self):
        client = RPCClient()

        responses.add(responses.POST, 'http://127.0.0.1:8880/',
                      json={'Found': 'Moved'}, status=302)

        response = client.get_height()
        self.assertTrue('Found' in response)

    def test_height(self):
        client = RPCClient()

        response = client.get_height()

        height = int(response)

        self.assertGreaterEqual(height, 0)

    def test_best_blockhash(self):
        client = RPCClient()

        hash = bytearray(binascii.unhexlify(client.get_best_blockhash()[2:]))
        hash.reverse()

        self.assertEqual(len(hash), 32)

    def test_getblockhash(self):
        client = RPCClient()

        height = 12344

        hash = client.get_block_hash(height)

        self.assertEqual(hash[2:], '1e67372c158a4cfbb17b9ad3aaae77001a4247a00318e354c62e53b56af4006f')

    def test_invoke(self):

        client = RPCClient()

        contract_hash = 'd7678dd97c000be3f33e9362e673101bac4ca654'
        params = [{'type': 7, 'value': 'symbol'}, {'type': 16, 'value': []}]

        result = client.invoke_contract(contract_hash, params)

        self.assertEqual(result['state'], 'HALT, BREAK')
        invoke_result = result['stack']
        self.assertEqual(len(invoke_result), 1)

        stack_item = invoke_result[0]

        self.assertEqual(stack_item['type'], 'ByteArray')
        self.assertEqual(binascii.hexlify('LWTF'.encode('utf-8')).decode('utf-8'), stack_item['value'])

    def test_send_raw_tx(self):
        client = RPCClient()

        raw_tx = '80000120d8edd2df8d6907caacd4af8872a596cb75c5829d015ce72895ce376d12def9a780ba502ae28ad7a4b7fbcf6baa4856edb537417d2a0000029b7cffdaa674beae0f930ebe6085af9093e5fe56b34a5c220ccdcf6efc336fc500a3e11100000000d8edd2df8d6907caacd4af8872a596cb75c5829d9b7cffdaa674beae0f930ebe6085af9093e5fe56b34a5c220ccdcf6efc336fc500bbeea000000000d8edd2df8d6907caacd4af8872a596cb75c5829d01414044dfd2b360e548607ece3d453173079233040c2484a99671a7346a8ca16969245b946bfa4c13125f4c931b0cbab216e0d241d908f37ad96abb776890832a3a4b2321025de86902ed42aca7246207a70869b22253aeb7cc84a4cb5eee3773fd78b3f339ac'

        # this will result in a false, since this tx has already been made
        # but, if it were badly formmated, it would be an error
        # so we are testing if we get back a false
        result = client.send_raw_tx(raw_tx)

        self.assertEqual(result, False)

    def test_get_version(self):
        client = RPCClient()
        version = client.get_version()
        self.assertIn("port", version)
        self.assertIn("nonce", version)
        self.assertIn("useragent", version)


class RPCEndPointTestCase(TestCase):

    def setUp(self):
        self.ep1 = RPCEndpoint(client=None, address='addr1')
        self.ep2 = RPCEndpoint(client=None, address='addr1')
        self.ep1.status = 200
        self.ep2.status = 200
        self.ep1.elapsed = 1
        self.ep2.elapsed = 1
        self.ep1.height = 1
        self.ep2.height = 1

    def test_eq(self):
        self.assertEquals(self.ep1, self.ep2)

    def test_gt_and_ge(self):
        self.ep2.height = 2
        self.assertGreater(self.ep1, self.ep2)
        self.ep2.height = 1
        self.assertGreaterEqual(self.ep1, self.ep2)

        self.ep1.status = 404
        self.assertGreater(self.ep2, self.ep1)

    def test_lt_and_le(self):
        self.ep2.height = 2
        self.assertLess(self.ep2, self.ep1)
        self.ep2.height = 1
        self.assertLessEqual(self.ep2, self.ep1)

    def test_str(self):
        self.assertEquals("[addr1] 200 1 1", str(self.ep1))
