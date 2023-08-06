import time
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin


@dataclass
class Event(DataClassJsonMixin):
    timestamp: float = field(
        default_factory=time.time,
        init=False,
        compare=False,
    )
