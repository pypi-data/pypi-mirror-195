from dataclasses import dataclass
from dataclasses import field


@dataclass
class Transfer(object):
    hash: bytearray = field(metadata={"required": True})
    method_id: str = field(metadata={"required": True})

    status: bool = field(metadata={"required": True})
    sender: str = field(metadata={"required": True})
    receiver: str = field(metadata={"required": True})
    symbol: str = field(metadata={"required": True})
    is_token: bool = field(metadata={"required": True})
    value: int = field(metadata={"required": True})

    trx_index: int = None
    block_number: int = None
    block_hash: bytearray = None
