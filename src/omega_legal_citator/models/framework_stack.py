from dataclasses import dataclass, field
from typing import List


@dataclass
class FrameworkStackClassification:
    stack_id: str
    label: str
    confidence: float
    signals: List[str] = field(default_factory=list)
    verification_status: str = "unverified"
