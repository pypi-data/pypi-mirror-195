from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class DefectPoint:
    defect_id: int
    point: Tuple[float, float] = field(default_factory=lambda: [])
    bin: int = -1
