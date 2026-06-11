from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


UNVERIFIED = "unverified"


@dataclass
class SourceProvenance:
    source_type: str
    retrieved_at: str
    source_id: Optional[str] = None
    source_url: Optional[str] = None
    content_hash: Optional[str] = None
    retrieval_notes: Optional[str] = None


@dataclass
class LegalProposition:
    proposition_id: str
    text: str
    framework_stack: Optional[str] = None
    confidence: Optional[float] = None
    notes: Optional[str] = None


@dataclass
class Authority:
    authority_id: str
    normalized_citation: str
    raw_text: str
    authority_type: str
    verification_status: str = UNVERIFIED
    title: Optional[str] = None
    court: Optional[str] = None
    reporter: Optional[str] = None
    provenance: List[SourceProvenance] = field(default_factory=list)
    confidence: Optional[float] = None
    notes: Optional[str] = None


@dataclass
class AuthorityLink:
    source_authority_id: str
    target_authority_id: str
    relationship: str
    verification_status: str = UNVERIFIED
    evidence: Optional[str] = None
    confidence: Optional[float] = None


def stable_authority_id(normalized_citation: str) -> str:
    token = normalized_citation.lower()
    token = "".join(character if character.isalnum() else "-" for character in token)
    token = "-".join(part for part in token.split("-") if part)
    return f"authority:{token}"


def as_public_dict(value: Any) -> Dict[str, Any]:
    return {
        key: item
        for key, item in value.__dict__.items()
        if item is not None and item != []
    }
