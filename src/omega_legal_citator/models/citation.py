from dataclasses import dataclass
from typing import Optional


@dataclass
class CitationObject:
    raw_text: str
    normalized_citation: str
    source_type: str
    retrieved_at: str
    citation_type: str = "case_reporter"
    verification_status: str = "unverified"
    court: Optional[str] = None
    reporter: Optional[str] = None
    authority_title: Optional[str] = None
    source_id: Optional[str] = None
    source_url: Optional[str] = None
    confidence: Optional[float] = None
    span_start: Optional[int] = None
    span_end: Optional[int] = None
    proposition_id: Optional[str] = None
    notes: Optional[str] = None
