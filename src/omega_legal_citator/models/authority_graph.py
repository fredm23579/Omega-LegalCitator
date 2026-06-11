from dataclasses import dataclass, field
from typing import Dict, List

from omega_legal_citator.models.authority import (
    Authority,
    AuthorityLink,
    SourceProvenance,
    as_public_dict,
    stable_authority_id,
)
from omega_legal_citator.models.citation import CitationObject


@dataclass
class AuthorityGraph:
    authorities: Dict[str, Authority] = field(default_factory=dict)
    links: List[AuthorityLink] = field(default_factory=list)

    def add_citation(self, citation: CitationObject) -> Authority:
        authority_id = stable_authority_id(citation.normalized_citation)
        provenance = SourceProvenance(
            source_type=citation.source_type,
            retrieved_at=citation.retrieved_at,
            source_id=citation.source_id,
            source_url=citation.source_url,
        )
        authority = self.authorities.get(authority_id)
        if authority is None:
            authority = Authority(
                authority_id=authority_id,
                normalized_citation=citation.normalized_citation,
                raw_text=citation.raw_text,
                authority_type=citation.citation_type,
                verification_status="unverified",
                title=citation.authority_title,
                court=citation.court,
                reporter=citation.reporter,
                confidence=citation.confidence,
                notes=citation.notes,
            )
            self.authorities[authority_id] = authority
        authority.provenance.append(provenance)
        return authority

    @classmethod
    def from_citations(cls, citations: List[CitationObject]) -> "AuthorityGraph":
        graph = cls()
        for citation in citations:
            graph.add_citation(citation)
        return graph

    def to_dict(self) -> dict:
        return {
            "authorities": {
                authority_id: {
                    **as_public_dict(authority),
                    "provenance": [as_public_dict(item) for item in authority.provenance],
                }
                for authority_id, authority in self.authorities.items()
            },
            "links": [as_public_dict(link) for link in self.links],
        }
