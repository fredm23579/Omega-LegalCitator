from dataclasses import dataclass
from typing import Optional


@dataclass
class CitationObject:
    raw_text: str
    normalized_citation: str
    source_type: str
    retrieved_at: str
    court: Optional[str] = None
    reporter: Optional[str] = None
    authority_title: Optional[str] = None
    source_id: Optional[str] = None
    source_url: Optional[str] = None
    confidence: Optional[float] = None
    notes: Optional[str] = None
