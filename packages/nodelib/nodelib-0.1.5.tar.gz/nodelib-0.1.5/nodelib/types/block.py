from dataclasses import dataclass
from dataclasses import field


@dataclass
class Block(object):
    number: int = field(metadata={"required": True})
    hash: bytearray = field(metadata={"required": True})

    transaction_count: int = field(metadata={"required": True})
