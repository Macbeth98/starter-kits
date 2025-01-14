"""Test the agent on a fork"""

import forta_agent
import pytest
import web3

import src.agent as agent
import tests.test_data as data

# FIXTURES ####################################################################

@pytest.fixture
def w3():
    return web3.Web3(web3.EthereumTesterProvider())

@pytest.fixture
def no_filter_handle_transaction(w3):
    return agent.handle_transaction_factory(w3=w3)

@pytest.fixture
def token_filter_handle_transaction(w3):
    return agent.handle_transaction_factory(w3=w3, target_token=data.TOKENS['Тether USD (USDТ)']) # fake token used for phishing

# RANDOM TX ###################################################################

def test_ignores_random_transactions(no_filter_handle_transaction):
    assert len(data.TRANSACTIONS['random']['any']) == 33
    assert all([len(no_filter_handle_transaction(_t)) == 0 for _t in data.TRANSACTIONS['random']['any']])

# BATCH ERC20 TRANSFERS #######################################################

def test_detects_native_tokens_batched_transfers(no_filter_handle_transaction):
    assert all([len(no_filter_handle_transaction(_t)) > 0 for _t in data.TRANSACTIONS['batch']['native']])

def test_detects_erc20_batched_transfers(no_filter_handle_transaction):
    assert all([len(no_filter_handle_transaction(_t)) > 0 for _t in data.TRANSACTIONS['batch']['ft']])

# FILTER BY TOKEN #############################################################

def test_filters_findings_by_token(token_filter_handle_transaction):
    assert len(token_filter_handle_transaction(data.TRANSACTIONS['batch']['ft'][0])) == 0
    assert len(token_filter_handle_transaction(data.TRANSACTIONS['batch']['ft'][1])) > 0 # the fake token is used in the second transaction
