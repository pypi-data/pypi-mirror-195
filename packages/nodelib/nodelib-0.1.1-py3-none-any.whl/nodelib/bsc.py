import logging
from typing import Any

from web3 import Web3
from .ether import EtherNode
from web3.middleware import geth_poa_middleware
from eth_account import Account

logger = logging.getLogger('nodes.bsc')


class BscNode(EtherNode):
    transfer_sigs = {
        'a9059cbb': ['transfer', 'address', 'uint256']
    }
    contract_symbols = {
        Web3.toChecksumAddress('0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82'): 'CAKE',
        Web3.toChecksumAddress('0xba2ae424d960c26247dd6c32edc70b295c744c43'): 'DOGE',
        Web3.toChecksumAddress('0x8fF795a6F4D97E7887C79beA79aba5cc76444aDf'): 'BCH',
        Web3.toChecksumAddress('0x1D2F0da169ceB9fC7B3144628dB156f3F6c60dBE'): 'XRP',
        Web3.toChecksumAddress('0x43a172c44dC55c2B45BF9436cF672850FC8bA046'): 'METAWAR',
        Web3.toChecksumAddress('0xf8a0bf9cf54bb92f17374d9e9a321e6a111a51bd'): 'LINK',
        Web3.toChecksumAddress('0x352Cb5E19b12FC216548a2677bD0fce83BaE434B'): 'BTT',
    }
    native_token = 'BNB'

    def __init__(self, uri: str, chain_id: int):
        super(BscNode, self).__init__(uri=uri, chain_id=chain_id)

        # inject the poa compatibility middleware to the innermost layer (0th layer)
        # @TODO: the following injection must happen before all other middleware_onion calls
        # ref: https://www.reddit.com/r/ethdev/comments/pbb536/estimating_a_gas_price_based_on_a_target_time_of/
        self._w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        logger.info('Injected geth_poa_middleware layer 0')

    def sign_function(self, function_call: Any, private_key: str):
        account = Account.from_key(private_key)

        # Prepare transaction
        _nonce = self._w3.eth.get_transaction_count(account.address)
        tx = {
            'chainId': self._chain_id,
            'nonce': _nonce,
            'from': account.address,
        }

        # Build transaction with function_call
        tx = function_call.build_transaction(tx)

        # Gas calculation
        tx['gas'] = self._w3.eth.estimate_gas(tx)
        tx['gasPrice'] = self._w3.eth.gas_price

        # sign the transaction
        signed_tx = self._w3.eth.account.sign_transaction(tx, private_key)

        return signed_tx['hash'], signed_tx

    def sign_transact(
            self, private_key: str, to_address: str, amount: int, fees_included: bool = False) -> tuple[bytearray, Any]:
        account = Account.from_key(private_key)

        # Prepare transaction
        _nonce = self._w3.eth.get_transaction_count(account.address)
        tx = {
            'chainId': self._chain_id,
            'nonce': _nonce,
            'from': account.address,
            'to': Web3.toChecksumAddress(to_address),
        }

        # Gas calculation
        tx['gas'] = self._w3.eth.estimate_gas(tx)
        tx['gasPrice'] = self._w3.eth.gas_price

        if fees_included:
            # Include the fees in the amount
            tx['value'] = amount - (tx['gas'] * tx['gasPrice'])
        else:
            tx['value'] = amount

        # sign the transaction
        signed_tx = self._w3.eth.account.sign_transaction(tx, private_key)

        return signed_tx['hash'], signed_tx
