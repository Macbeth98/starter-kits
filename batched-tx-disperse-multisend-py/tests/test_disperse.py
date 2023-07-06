"""Test the transaction parsing for the Disperse contract"""

import pytest
import web3

import src.disperse as disperse

# FIXTURES ####################################################################

TOKENS = {
    'fake': '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
    'ilv': '0x767fe9edc9e0df98e07454847909b5e959d7ca0e',
}

TRANSACTION_INPUTS = {
    'random-data': '0xa9059cbb0000000000000000000000006dfc34609a05bc22319fa4cce1d1e2929548c0d700000000000000000000000000000000000000000000000000000000017fc230',
    'disperse-eth': '0xe63d38ed000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000002e000000000000000000000000000000000000000000000000000000000000000140000000000000000000000007de08abcf75f08aaf6eefa239fe479d26597db4e000000000000000000000000af33273f0d7d18a87f737de95a8fb00c545f4ff500000000000000000000000031612a75f5d646d82b4100d1578019eefb698dee00000000000000000000000077b3ddb51c776bc11af0d7240a02fe9e46a03340000000000000000000000000eb60c48a1aea8a84d3333962d8fb6529f2a3ef8a000000000000000000000000dcba1d220959402eb1ad903cb6b50aefb30b03ae000000000000000000000000a88b2947650c1c45e6cf97a895e48e0c8ddbf3d7000000000000000000000000df2dcf3c6bb807116d2ad70d0641d1f504903964000000000000000000000000c864fca1e9b3f2bdd0c8206400f3f6530adcdca3000000000000000000000000195ad1dad0525f906d91319fbb22ab0288a6b879000000000000000000000000fd80e81df83f34312d966496ea943cf57070f0ea000000000000000000000000be231b29968b25bbacb146f9debb5e56b443ce7b00000000000000000000000096e0e0f11a6f1a2c268990067da6d4e0fa851846000000000000000000000000ec68a45f709735994e5340a73b74a7f53bd7bd470000000000000000000000009dd577a45c4daa73ed2cb993740a9953fca996d2000000000000000000000000e3cd01d3372a917986f118161abc00a5497eb425000000000000000000000000dfb92ff48aafa9d4f4cc6877b8df0752e063a3230000000000000000000000004da2facee5eb9f40da6fcb86a3264cc777ffc60f00000000000000000000000084b8aeca2dadb97a3a7e2cba0899fe1e13e6152e0000000000000000000000008908f93a43000a270f9e4f8cbde6671ccc21fc2600000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a00000000000000000000000000000000000000000000000000000f6bc6833a6a0000',
    'disperse-token': '0xc73a2d60000000000000000000000000767fe9edc9e0df98e07454847909b5e959d7ca0e000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000001e0000000000000000000000000000000000000000000000000000000000000000b00000000000000000000000007f3eaa03c2deb2b909b7ff5ecf4a20f540ab1de0000000000000000000000004c956623424394c5dc4fd71f04bb28ee117b496f00000000000000000000000077d880c57f0aafea9f41405098dbe60b538cfa750000000000000000000000004eaec98a381fb95067278b1bec977b83a501dd2f000000000000000000000000380846d771c1fc8a0f7724ee98f86e2127474239000000000000000000000000fe5a0a6eca55ce3c0343a447b779ab4346c801a70000000000000000000000002174974d39141d4293c38a9b7be5b915a746ea44000000000000000000000000fe5a0a6eca55ce3c0343a447b779ab4346c801a70000000000000000000000006b2dd9587357b1bd0e7540c48733960b3e873606000000000000000000000000ac93e5f3c1512dba1eb5eed0136ccaaf31d04561000000000000000000000000f7845cc3d24a511e15a0368871465f0dc5ae4fb1000000000000000000000000000000000000000000000000000000000000000b00000000000000000000000000000000000000000000000783b5d2d0cfb7a800000000000000000000000000000000000000000000000003e576f0bd8eb94000000000000000000000000000000000000000000000000003e576f0bd8eb940000000000000000000000000000000000000000000000000064320080e66c56800000000000000000000000000000000000000000000000004ded4acecf26790000000000000000000000000000000000000000000000000070a6b2637cf783800000000000000000000000000000000000000000000000007036fb155341a400000000000000000000000000000000000000000000000000703a2c351b4bfb0000000000000000000000000000000000000000000000000070706f4b91de08000000000000000000000000000000000000000000000000003e8db2232f02168000000000000000000000000000000000000000000000000137b52b3b3c99e4000',
}

@pytest.fixture
def w3():
    return web3.Web3(web3.EthereumTesterProvider())

@pytest.fixture
def base_parser(w3):
    return disperse.parse_transaction_input_factory(w3=w3)

@pytest.fixture
def random_token_filter_parser(w3):
    return disperse.parse_transaction_input_factory(w3=w3, token=TOKENS['fake'])

@pytest.fixture
def matching_token_filter_parser(w3):
    return disperse.parse_transaction_input_factory(w3=w3, token=TOKENS['ilv'])

# DATA CORRUPTION #############################################################

def test_does_not_throw_on_random_data(base_parser):
    _r = base_parser(TRANSACTION_INPUTS['random-data'])
    assert len(_r) == 2 # valid output
    assert len(_r[0]) == 0 # no token identified
    assert len(_r[1]) == 0 # no transfers

# ETH #########################################################################

def test_parses_recipients_and_values_from_batch_eth_transaction(base_parser):
    _r = base_parser(TRANSACTION_INPUTS['disperse-eth'])
    assert len(_r) == 2 # valid output
    assert len(_r[0]) == 0 # no token identified, since ETH is native
    assert len(_r[1]) > 0 # found batched transfers

# ERC20 #######################################################################

def test_parses_recipients_and_values_from_batch_erc20_transaction(base_parser):
    _r = base_parser(TRANSACTION_INPUTS['disperse-token'])
    assert len(_r) == 2 # valid output
    assert len(_r[0]) > 0 # found an ERC20 token
    assert len(_r[1]) > 0 # found batched transfers

# FILTER ERC20 ################################################################

def test_removes_findings_that_dont_match_token_filter(random_token_filter_parser):
    _r = random_token_filter_parser(TRANSACTION_INPUTS['disperse-token'])
    assert len(_r) == 2 # valid output
    assert len(_r[0]) > 0 # found an ERC20 token
    assert len(_r[1]) == 0 # no transfers for the target token

def test_keeps_findings_that_match_token_filter(matching_token_filter_parser):
    _r = matching_token_filter_parser(TRANSACTION_INPUTS['disperse-token'])
    assert len(_r) == 2 # valid output
    assert len(_r[0]) > 0 # token match
    assert len(_r[1]) > 0 # transfers for the target token
