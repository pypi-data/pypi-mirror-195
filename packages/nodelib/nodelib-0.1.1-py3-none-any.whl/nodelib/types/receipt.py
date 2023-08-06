from dataclasses import dataclass
from dataclasses import field


@dataclass
class Receipt(object):
    hash: bytearray = field(metadata={"required": True})

    status: bool = field(metadata={"required": True})
    fee: int = field(metadata={"required": True})
