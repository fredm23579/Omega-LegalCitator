from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CitationAuditFinding:
    finding_id: str
    severity: str
    category: str
    message: str
    citation: Optional[str] = None
    authority_title: Optional[str] = None
    expected_citation: Optional[str] = None
    blocks_release: bool = False


@dataclass
class CitationAuditReport:
    findings: List[CitationAuditFinding] = field(default_factory=list)

    @property
    def has_blockers(self) -> bool:
        return any(finding.blocks_release for finding in self.findings)

    def to_dict(self) -> dict:
        return {
            "has_blockers": self.has_blockers,
            "findings": [
                {key: value for key, value in finding.__dict__.items() if value is not None}
                for finding in self.findings
            ],
        }
