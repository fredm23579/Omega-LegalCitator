import re
from typing import List

from omega_legal_citator.models.citation import CitationObject


BASIC_CASE_CITATION = re.compile(r"\b\d+\s+[A-Z][A-Za-z.0-9]*\s+\d+\b")


def extract_basic_citations(text: str, source_type: str = "web", retrieved_at: str = "") -> List[CitationObject]:
    citations = []
    for match in BASIC_CASE_CITATION.finditer(text):
        raw = match.group(0)
        citations.append(
            CitationObject(
                raw_text=raw,
                normalized_citation=raw,
                source_type=source_type,
                retrieved_at=retrieved_at,
            )
        )
    return citations
