from abc import ABCMeta, abstractmethod
from typing import Sequence, Union, Any

from .types import Block, Transfer, Receipt


class INode(metaclass=ABCMeta):
    transfer_sigs = {}
    contract_symbols = {}
    native_token = None
    default_abi = {}

    def __init__(self, uri: str):
        self._uri = uri

    def reset_contract_symbols(self):
        self.contract_symbols = {}

    @abstractmethod
    def add_contract_symbol(self, contract_address: str, symbol: str):
        """Append to self.contract_symbols"""

    @abstractmethod
    def last_block_number(self) -> int:
        """Get the last block number on chain"""

    @abstractmethod
    def status(self) -> bool:
        """Indicate node status"""

    @staticmethod
    @abstractmethod
    def get_new_private_key() -> str:
        """Generate a new private key"""

    @staticmethod
    @abstractmethod
    def get_address_from_privatekey(private_key: str) -> str:
        """Get address from private_key"""

    @staticmethod
    @abstractmethod
    def get_address_from_publickey(public_key: str) -> str:
        """Get address from public_key"""

    @abstractmethod
    def get_contract(self, contract_address: str, _abi: list):
        """Returns a contract object"""

    @abstractmethod
    def get_balance(self, address: str, contract_address: str = None, abi: str = None) -> int:
        """Return account balance using public address"""

    @abstractmethod
    def get_block(self, block_identifier: int) -> Block:
        """Get block by number"""

    @abstractmethod
    def get_transfer(
            self, tx_hash: bytearray = None, transaction: dict = None) -> Union[Transfer, None]:
        """Get a Transfer object from an already obtained transaction or by looking up using transaction hash"""

    @abstractmethod
    def get_transfers(self, block_identifier: int) -> Sequence[Transfer]:
        """Get Transfer transactions in a block by number"""

    @abstractmethod
    def get_transaction_receipt(self, tx_hash: str) -> Union[Receipt, None]:
        """Return a Receipt Dto of a transaction by hash"""

    @abstractmethod
    def send_and_get_receipt(self, signed_tx) -> bytearray:
        """Send the transaction and return the receipt"""

    @abstractmethod
    def sign_function(self, function_call: Any, private_key: str):
        """Sign a function call"""

    @abstractmethod
    def sign_transact(
            self, private_key: str, to_address: str, amount: int, fees_included: bool = False) -> tuple[bytearray, Any]:
        """Sign a transaction and return transaction hash and transaction object
        If amount is None, then the balance will be transferred totally to to_address"""

    @abstractmethod
    def sign_transfer(self, private_key: str, to_address: str, amount: int,
                      contract_address: str, abi: str = None) -> tuple[bytearray, Any]:
        """Execute smart contract's transfer function and return transaction hash and transaction object"""
