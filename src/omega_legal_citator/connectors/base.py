from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SourceRecord:
    source_type: str
    source_id: str | None
    source_url: str | None
    payload: Dict[str, Any]


class BaseConnector:
    source_name = "base"

    def describe(self) -> dict:
        return {"source_name": self.source_name}

    def collect(self, query: str) -> list[SourceRecord]:
        raise NotImplementedError
