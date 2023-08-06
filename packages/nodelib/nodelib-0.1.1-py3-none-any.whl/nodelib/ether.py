import logging
from typing import Sequence, Union, Any

from .interface import INode
import secrets
from cachetools import cached, TTLCache
from eth_account import Account
from eth_abi import abi
from web3 import Web3
from web3.exceptions import TransactionNotFound
from web3.providers import HTTPProvider
from web3.gas_strategies.time_based import construct_time_based_gas_price_strategy
from web3 import middleware

from hexbytes import HexBytes

from .types import Block, Transfer, Receipt
from automapper import mapper

logger = logging.getLogger('nodes.ether')

is_contract_cache = TTLCache(maxsize=500, ttl=3600)


class EtherNode(INode):
    transfer_sigs = {
        'a9059cbb': ['transfer', 'address', 'uint256']
    }
    contract_symbols = {
        Web3.toChecksumAddress('0x0d8775f648430679a709e98d2b0cb6250d2887ef'): 'BAT',
        Web3.toChecksumAddress('0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce'): 'SHIB',
        Web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7'): 'USDT',
        Web3.toChecksumAddress('0x2af5d2ad76741191d15dfe7bf6ac92d4bd912ca3'): 'LEO',
        Web3.toChecksumAddress('0xa0b73e1ff0b80914ab6fe0444e65848c4c34450b'): 'CRO',
        Web3.toChecksumAddress('0x6f259637dcd74c767781e37bc6133cd6a68aa161'): 'HT',
        Web3.toChecksumAddress('0x3506424f91fd33084466f402d5d97f05f8e3b4af'): 'CHZ',
        Web3.toChecksumAddress('0x0f5d2fb29fb7d3cfee444a200298f468908cc942'): 'MANA',
        Web3.toChecksumAddress('0xb62132e35a6c13ee1ee0f84dc5d40bad8d815206'): 'NEXO',
        Web3.toChecksumAddress('0x514910771af9ca656af840dff83e8264ecf986ca'): 'LINK',
        Web3.toChecksumAddress('0xc669928185dbce49d2230cc9b0979be6dc797957'): 'BTT',
    }
    native_token = 'ETH'
    default_abi = {
        'transfer': [
            {"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}],
             "name": "transfer", "outputs": [{"name": "success", "type": "bool"}], "payable": False,
             "stateMutability": "nonpayable", "type": "function"}],
        'balanceOf': [
            {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf",
             "outputs": [{"name": "balance", "type": "uint256"}], "payable": False, "stateMutability": "view",
             "type": "function"}]
    }
    miner_fee_percent = 0.02

    def __init__(self, uri: str, chain_id: int, max_wait_seconds: int = 60, sample_size: int = 3,
                 probability: int = 95):
        super(EtherNode, self).__init__(uri=uri)
        logger.debug('Instantiating EtherNode (chainId: %s) with uri: %s', chain_id, uri)
        self._w3 = Web3(HTTPProvider(endpoint_uri=self._uri))

        # Set gas pricing strategy
        self._w3.eth.set_gas_price_strategy(
            construct_time_based_gas_price_strategy(
                max_wait_seconds=max_wait_seconds, sample_size=sample_size, probability=probability))

        # Use cacheing
        self._w3.middleware_onion.add(middleware.time_based_cache_middleware)
        self._w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
        self._w3.middleware_onion.add(middleware.simple_cache_middleware)

        logger.info('Instanced %s client: %s', self.__class__.__name__, self._w3.clientVersion)

        self._chain_id = chain_id

    def add_contract_symbol(self, contract_address: str, symbol: str):
        self.contract_symbols[Web3.toChecksumAddress(contract_address)] = symbol.upper()

    def last_block_number(self) -> int:
        return self._w3.eth.block_number

    def status(self) -> bool:
        return self._w3.isConnected()

    @staticmethod
    def get_new_private_key() -> str:
        return secrets.token_hex(32)

    @staticmethod
    def get_address_from_privatekey(private_key: str) -> str:
        return Web3.toChecksumAddress(Account.from_key(private_key).address)

    @staticmethod
    def get_address_from_publickey(public_key: str) -> str:
        _h = Web3.keccak(hexstr='%s' % public_key)
        return Web3.toChecksumAddress("0x%s" % _h.hex()[-40:])

    def get_contract(self, contract_address: str, _abi: list):
        contract = self._w3.eth.contract(
            Web3.toChecksumAddress(contract_address), abi=_abi)

        return contract

    def get_balance(self, address: str, contract_address: str = None, _abi: str = None) -> int:
        if contract_address is None:
            # Return native token balance
            return self._w3.eth.get_balance(Web3.toChecksumAddress(address))

        # Call the balanceOf function of the smart contract
        contract = self._w3.eth.contract(
            Web3.toChecksumAddress(contract_address),
            abi=self.default_abi.get('balanceOf', None) if _abi is None else _abi)

        return contract.functions.balanceOf(
            Web3.toChecksumAddress(address)).call()

    def get_block(self, block_identifier: int) -> Block:
        _block = self._w3.eth.get_block(block_identifier)

        return mapper.to(Block).map(_block, use_deepcopy=False, fields_mapping={
            "transaction_count": len(_block.transactions)
        })

    @cached(is_contract_cache)
    def is_contract(self, address: str) -> bool:
        """The best way to detect if address is a contract or a wallet is to check if it has
        a contract bytecode, while this call is slow, caching is needed."""
        if self._w3.eth.get_code(address) != b'':
            return True
        else:
            return False

    def get_transfer(
            self, tx_hash: bytearray = None, transaction: dict = None) -> Union[Transfer, None]:
        if transaction is None and tx_hash is None:
            # At least, one of the args must be provided
            return None

        if tx_hash is not None and transaction is None:
            try:
                # Get transaction from chain
                transaction = self._w3.eth.get_transaction(tx_hash)
            except TransactionNotFound:
                return None

        if 'to' not in transaction or transaction.to is None:
            # A transaction without a 'to' address cannot be a transfer
            return None

        # Convert transaction to Transfer
        transfer = None
        # Checking if the receiver is a contract address ?
        contract_symbol = self.contract_symbols.get(Web3.toChecksumAddress(transaction.to), None)
        # Calling the is_contract() is expensive (even it's cached), it is now replaced
        # by simply checking if it's a contract we know (provisioned in self.contract_symbols)
        # all other transactions will be considered as native token transactions, this is
        # acceptable when we're looking for transactions from/to -WATCHED- addresses only.
        #if contract_symbol is None and not self.is_contract(transaction.to):
        if contract_symbol is None:
            transfer = mapper.to(Transfer).map(transaction, use_deepcopy=False, fields_mapping={
                "trx_index": transaction.transactionIndex,
                "hash": HexBytes(transaction.hash),
                "method_id": 'Transfer',
                "sender": Web3.toChecksumAddress(transaction.get('from')),
                "receiver": Web3.toChecksumAddress(transaction.to),
                "block_number": transaction.blockNumber,
                "block_hash": HexBytes(transaction.blockHash),
                "value": transaction['value'],
                "symbol": self.native_token,
                "is_token": False,
                "status": None
            })
        elif contract_symbol is not None:
            # We have a smart contract here
            _tx_data = transaction['input']
            transfer_sig = self.transfer_sigs.get(_tx_data[2:][:8], None)

            # Is it a transfer ?
            if transfer_sig is not None:
                function_args = transfer_sig[1:]

                # Get transaction inputs
                inputs = abi.decode(
                    [_ for _ in function_args], bytearray.fromhex(_tx_data[10:]))

                transfer = mapper.to(Transfer).map(transaction, use_deepcopy=False, fields_mapping={
                    "trx_index": transaction.transactionIndex,
                    "hash": HexBytes(transaction.hash),
                    "method_id": '%s(%s)' % (transfer_sig[0], [_ for _ in function_args]),
                    "sender": Web3.toChecksumAddress(transaction.get('from')),
                    "receiver": Web3.toChecksumAddress(inputs[0]),
                    "block_number": transaction.blockNumber,
                    "block_hash": HexBytes(transaction.blockHash),
                    "value": inputs[1],
                    "symbol": contract_symbol,
                    "is_token": True,
                    "status": None
                })

        return transfer

    def get_transfers(self, block_identifier: int) -> Sequence[Transfer]:
        _transactions = self._w3.eth.get_block(block_identifier, full_transactions=True).get('transactions', [])

        transfers = []
        for _transaction in _transactions:
            transfer = self.get_transfer(transaction=_transaction)

            # Validations
            if transfer is None:
                continue
            if transfer.receiver is None:
                logger.error("Ignoring transfer %s in block #%s: undefined 'to' key",
                             transfer.trx_index, block_identifier)
                continue
            if transfer.receiver == transfer.sender:
                logger.warning("Ignoring transfer %s in block #%s: from == to",
                               transfer.trx_index, block_identifier)
                continue

            transfers.append(transfer)

        return transfers

    def get_transaction_receipt(self, tx_hash: str) -> Union[Receipt, None]:
        try:
            # Get transaction's receipt info from chain
            _receipt = self._w3.eth.get_transaction_receipt(tx_hash)
        except TransactionNotFound:
            return None

        return mapper.to(Receipt).map(_receipt, use_deepcopy=False, fields_mapping={
            "hash": _receipt.transactionHash,
            "status": True if _receipt.get('status', 0) == 1 else False,
            "fee": _receipt.effectiveGasPrice * _receipt.gasUsed,
        })

    def estimate_transact_fee(self, tx: dict) -> tuple[int, int, int]:
        # Gas calculation
        gas_estimate = self._w3.eth.estimate_gas(tx)
        # ref: https://docs.alchemy.com/docs/maxpriorityfeepergas-vs-maxfeepergas#what-is-maxfeepergas-a-hrefand-finally-what-is-max-fee-per-gas-idand-finally-what-is-max-fee-per-gasa
        # Reminder:
        # maxPriorityFeePerGas = Spent for miner tips
        # maxFeePerGas = Spent in total per unit of gas
        base_fee_per_gas = int(self._w3.eth.get_block('latest').baseFeePerGas)
        # max_priority_fee_per_gas = int(self._w3.eth.max_priority_fee)
        max_priority_fee_per_gas = int(base_fee_per_gas * self.miner_fee_percent)  # miner's percent from base_fee_per_gas
        max_fee_per_gas = base_fee_per_gas + max_priority_fee_per_gas

        # Returns: gas_estimate, max_fee_per_gas, max_priority_fee_per_gas
        return gas_estimate, max_fee_per_gas, max_priority_fee_per_gas

    def send_and_get_receipt(self, signed_tx) -> tuple[HexBytes, Any]:
        # Send it
        sent_tx = self._w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Wait for receipt
        tx_receipt = self._w3.eth.wait_for_transaction_receipt(sent_tx)

        return tx_receipt.transactionHash, tx_receipt

    def sign_function(self, function_call: Any, private_key: str):
        account = Account.from_key(private_key)

        # Prepare transaction
        _nonce = self._w3.eth.get_transaction_count(account.address)
        tx = {
            'chainId': self._chain_id,
            'nonce': _nonce,
            'from': account.address,
            'type': 0x2
        }

        # Build transaction with function_call
        tx = function_call.build_transaction(tx)

        # Gas calculation
        # Based on:
        # https://ethereum.stackexchange.com/questions/128536/how-do-node-providers-e-g-infura-alchemy-determine-gas-pricing-on-contract-w
        last_block = self._w3.eth.get_block('latest')
        del(tx['gasPrice'])
        tx['maxPriorityFeePerGas'] = 1000000000
        tx['maxFeePerGas'] = (last_block['baseFeePerGas'] * 2) + tx['maxPriorityFeePerGas']
        #tx['gas'] = self._w3.eth.estimate_gas(tx)
        #tx['gasPrice'] = self._w3.eth.gas_price

        # sign the transaction
        signed_tx = self._w3.eth.account.sign_transaction(tx, private_key)

        return signed_tx['hash'], signed_tx

    def sign_transact(
            self, private_key: str, to_address: str, amount: int, fees_included: bool = False) -> tuple[bytearray, Any]:
        account = Account.from_key(private_key)

        # Gas calculation
        _gas_price = None
        _gas, _max_fee_per_gas, _max_priority_fee_per_gas = self.estimate_transact_fee({'to': to_address})

        if fees_included:
            # Include the fees in the amount
            # Make a transaction with type 0x1
            _gas_price = self._w3.eth.gas_price
            amount = amount - (_gas * _gas_price)

        # Prepare transaction
        _nonce = self._w3.eth.get_transaction_count(account.address)
        tx = {
            'chainId': self._chain_id,
            'nonce': _nonce,
            'from': account.address,
            'to': Web3.toChecksumAddress(to_address),
            'value': amount,
            'gas': _gas,
        }

        if _gas_price is None:
            tx['type'] = '0x2'
            tx['maxFeePerGas'] = _max_fee_per_gas
            tx['maxPriorityFeePerGas'] = _max_priority_fee_per_gas
        else:
            tx['type'] = '0x1'
            tx['gasPrice'] = _gas_price

        # sign the transaction
        signed_tx = self._w3.eth.account.sign_transaction(tx, private_key)

        return signed_tx['hash'], signed_tx

    def sign_transfer(self, private_key: str, to_address: str, amount: int,
                      contract_address: str, abi: str = None) -> tuple[bytearray, Any]:
        # Prepare contract
        contract = self._w3.eth.contract(
            Web3.toChecksumAddress(contract_address),
            abi=self.default_abi.get('transfer', None) if abi is None else abi)

        function_call = contract.functions.transfer(
            Web3.toChecksumAddress(to_address), amount)

        return self.sign_function(function_call, private_key)
