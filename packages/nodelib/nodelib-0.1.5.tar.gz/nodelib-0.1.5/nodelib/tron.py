import logging
import codecs
import base58

from typing import Sequence, Union, Any

from hexbytes import HexBytes

from automapper import mapper

from .interface import INode
from Crypto.Hash import keccak
from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey
from tronpy.abi import trx_abi
from tronpy.exceptions import TransactionNotFound

from .types import Block, Transfer, Receipt

logger = logging.getLogger('nodes.tron')


def keccak256(data: bytes) -> bytes:
    hasher = keccak.new(digest_bits=256)
    hasher.update(data)
    return hasher.digest()


class TronNode(INode):
    transfer_sigs = {
        'a9059cbb': ['transfer', 'address', 'uint256']
    }
    contract_symbols = {
        'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t': 'USDT',
        'TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4': 'BTT'
    }
    native_token = 'TRX'
    default_abi = {
        'transfer': [
            {"outputs": [{"type": "bool"}],
             "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}],
             "name": "transfer", "stateMutability": "Nonpayable", "type": "Function"}],
        'balanceOf': [{"constant": True, "inputs": [{"name": "who", "type": "address"}],
                       "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}],
                       "payable": False, "stateMutability": "view", "type": "function"}]
    }

    def __init__(self, uri):
        super(TronNode, self).__init__(uri=uri)
        logger.debug('Instantiating TronNode with uri: %s', uri)
        self._tron = Tron(HTTPProvider(self._uri))
        logger.info('Instanced %s client: versionNum=%s',
                    self.__class__.__name__,
                    self._tron.get_node_info().get('configNodeInfo').get('versionNum'))

    def add_contract_symbol(self, contract_address: str, symbol: str):
        self.contract_symbols[contract_address] = symbol.upper()

    def last_block_number(self) -> int:
        return self._tron.get_latest_block_number()

    def status(self):
        try:
            # tronpy does not provide a status, this is a workaround to return a status
            self._tron.get_latest_block_number()
        except Exception as e:
            logger.error('TronNode status() raised error (%s): %s', e.__class__.__name__, e)
            return False
        else:
            return True

    @staticmethod
    def get_new_private_key() -> str:
        return '%s' % PrivateKey.random()

    @staticmethod
    def get_address_from_privatekey(private_key: str) -> str:
        return PrivateKey(bytes.fromhex(private_key)).public_key.to_base58check_address()

    @staticmethod
    def get_address_from_publickey(public_key: str) -> str:
        _h = keccak256(bytes.fromhex(public_key))
        _hex = '41%s' % _h.hex()[-40:]
        return base58.b58encode_check(bytes.fromhex(_hex)).decode('utf-8')

    def get_contract(self, contract_address: str, _abi: list):
        contract = self._tron.get_contract(contract_address)
        contract.abi = _abi

        return contract

    def get_balance(self, address: str, contract_address: str = None, abi: str = None) -> int:
        if contract_address is None:
            # Return native token balance
            _decimal_balance = self._tron.get_account_balance(address)
            return int(str(_decimal_balance).replace('.', ''))

        # Call the balanceOf function of the smart contract
        # Prepare contract
        contract = self.get_contract(
            contract_address,
            self.default_abi.get('balanceOf', None) if abi is None else abi)

        return contract.functions.balanceOf(address)

    def get_bandwidth(self, address: str) -> int:
        _account_resource = self._tron.get_account_resource(address)
        return _account_resource.get('freeNetLimit', 0) - _account_resource.get('freeNetUsed', 0)

    def get_block(self, block_identifier: int) -> Block:
        _block = self._tron.get_block(block_identifier)

        return mapper.to(Block).map(_block, use_deepcopy=False, fields_mapping={
            "number": _block['block_header']['raw_data']['number'],
            "hash": HexBytes(codecs.decode(_block['blockID'], 'hex_codec')),
            "transaction_count": len(_block.get('transactions', []))
        })

    def get_transfer(
            self, tx_hash: bytearray = None, transaction: dict = None) -> Union[Transfer, None]:
        if transaction is None and tx_hash is None:
            # At least, one of the args must be provided
            return None

        if tx_hash is not None and transaction is None:
            try:
                # Get transaction from chain
                transaction = self._tron.get_transaction(tx_hash)
            except TransactionNotFound:
                return None

        _contracts_len = len(transaction['raw_data']['contract'])
        if _contracts_len != 1:
            # Ref: https://stackoverflow.com/questions/64373633/what-is-the-case-where-you-need-multiple-contracts-results-for-a-single-transact
            logger.error("Ignoring transaction %s in block #%s: contracts = %s",
                         transaction['txID'], transaction['block_number'], _contracts_len)
            return None

        # Convert transaction to Transfer
        transfer = None
        _contract = transaction['raw_data']['contract'][0]
        if _contract['type'] == 'TransferContract':
            # Ignoring TransferAssetContract by now since it holds TRC-10 transfers
            # ref: https://github.com/tronprotocol/documentation/blob/master/English_Documentation/TRON_Virtual_Machine/TRC10_TRX_TRANSFER_INTRODUCTION_FOR_EXCHANGES.md

            transfer = mapper.to(Transfer).map(transaction, use_deepcopy=False, fields_mapping={
                "hash": HexBytes(codecs.decode(transaction['txID'], 'hex_codec')),
                "method_id": 'Transfer',
                "sender": _contract['parameter']['value']['owner_address'],
                "receiver": _contract['parameter']['value']['to_address'],
                "value": _contract['parameter']['value']['amount'],
                "symbol": self.native_token,
                "is_token": False,
                "status": transaction['ret'][0]['contractRet']
            })
        elif _contract['type'] == 'TriggerSmartContract' and 'data' in _contract['parameter']['value']:
            _tx_data = _contract['parameter']['value']['data']
            contract_symbol = self.contract_symbols.get(_contract['parameter']['value']['contract_address'], None)
            transfer_sig = self.transfer_sigs.get(_tx_data[:8], None)

            # Is it a transfer ?
            if contract_symbol is not None and transfer_sig is not None:
                function_args = transfer_sig[1:]

                # Workaround to avoid padding issue
                # Ref: https://github.com/ethereum/eth-abi/issues/116
                if function_args[0] == 'address' and _tx_data[8:][:24] == '000000000000000000000041':
                    _tx_data = _tx_data[:8] + '000000000000000000000000' + _tx_data[8:][24:]

                # Get transaction inputs
                inputs = trx_abi.decode_abi(
                    [_ for _ in function_args], bytearray.fromhex(_tx_data[8:]))

                transfer = mapper.to(Transfer).map(transaction, use_deepcopy=False, fields_mapping={
                    "hash": HexBytes(codecs.decode(transaction['txID'], 'hex_codec')),
                    "method_id": '%s(%s)' % (transfer_sig[0], [_ for _ in function_args]),
                    "sender": _contract['parameter']['value']['owner_address'],
                    "receiver": inputs[0],
                    "value": inputs[1],
                    "symbol": contract_symbol,
                    "is_token": True,
                    "status": transaction['ret'][0]['contractRet']
                })

        return transfer

    def get_transfers(self, block_identifier: int) -> Sequence[Transfer]:
        _block = self._tron.get_block(block_identifier)
        _transactions = _block.get('transactions', [])

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
        if tx_hash[:2] == '0x':
            tx_hash = tx_hash[2:]

        try:
            # Get transaction info from chain
            _transaction_info = self._tron.get_transaction_info(tx_hash)
        except TransactionNotFound:
            return None

        _status = True
        if 'result' in _transaction_info and _transaction_info['result'] != 'SUCCESS':
            _status = False

        return mapper.to(Receipt).map(_transaction_info, use_deepcopy=False, fields_mapping={
            "hash": _transaction_info['id'],
            "status": _status,
            "fee": _transaction_info.get('fee', 0),
        })

    def send_and_get_receipt(self, signed_tx) -> tuple[HexBytes, Any]:
        broadcasted_tx = signed_tx.broadcast().wait()

        return HexBytes(codecs.decode(broadcasted_tx['id'], 'hex_codec')), broadcasted_tx

    def sign_function(self, function_call: Any, private_key: str):
        pk = PrivateKey(bytes.fromhex(private_key))

        function_call.sign(pk)

        return bytes.fromhex(function_call.txid), function_call

    def sign_transact(
            self, private_key: str, to_address: str, amount: int, fees_included: bool = False) -> tuple[bytearray, Any]:
        pk = PrivateKey(bytes.fromhex(private_key))

        if fees_included:
            # Include the fees in the amount
            # @TODO: are we going to consume TRX for this transaction or just bandwidth ?
            amount = amount

        tx = (
            self._tron.trx.transfer(
                pk.public_key.to_base58check_address(),
                to_address,
                amount)
            .build()
            .sign(pk)
        )

        return bytes.fromhex(tx.txid), tx

    def sign_transfer(self, private_key: str, to_address: str, amount: int,
                      contract_address: str, abi: str = None) -> tuple[bytearray, Any]:
        pk = PrivateKey(bytes.fromhex(private_key))

        # Prepare contract
        contract = self.get_contract(
            contract_address,
            self.default_abi.get('transfer', None) if abi is None else abi)

        # Base tx
        call_tx = (
            contract.functions.transfer(
                to_address,
                amount)
            .with_owner(pk.public_key.to_base58check_address())
            .build()
        )

        return self.sign_function(call_tx, private_key)

    def freeze(self, private_key: str, amount: int, resource: str = 'ENERGY') -> HexBytes:
        pk = PrivateKey(bytes.fromhex(private_key))

        tx = (
            self._tron.trx.freeze_balance(
                pk.public_key.to_base58check_address(),
                amount,
                resource
            )
            .build()
            .sign(pk)
        )

        logger.debug("Broadcasting freeze trx: %s", tx)
        broadcasted_tx = tx.broadcast().wait()
        logger.info(
            "Freeze %s TRX from %s for %s, hash=%s",
            amount, pk.public_key.to_base58check_address(), resource, broadcasted_tx['id']
        )

        return HexBytes(codecs.decode(broadcasted_tx['id'], 'hex_codec'))
