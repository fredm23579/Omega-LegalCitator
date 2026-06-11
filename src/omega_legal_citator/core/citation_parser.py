import re
from typing import Iterable, List, Tuple

from omega_legal_citator.models.citation import CitationObject


BASIC_CASE_CITATION = re.compile(r"\b\d+\s+[A-Z][A-Za-z.0-9]*\s+\d+\b")
USC_CITATION = re.compile(r"\b\d+\s+U\.S\.C\.\s+§+\s*[\w().-]+\b")
CFR_CITATION = re.compile(r"\b\d+\s+C\.F\.R\.\s+§+\s*[\w().-]+\b")
FED_RULE_CITATION = re.compile(r"\bFed\.\s+R\.\s+(?:Civ|Crim|Evid|App)\.\s+P\.\s+\d+(?:\([a-z0-9]+\))*\b")
CONSTITUTIONAL_CITATION = re.compile(r"\bU\.S\.\s+Const\.\s+amend\.\s+[IVXLCDM]+\b")
TITLE_WORD = r"[A-Z][A-Za-z0-9.'&-]+"
TITLE_CONNECTOR = r"(?:of|the|and|for|in|on|to|by|from|with|as|at|de|del|la|le|van|von)"
PARTY_NAME = rf"{TITLE_WORD}(?:\s+(?:{TITLE_CONNECTOR}\s+)?{TITLE_WORD})*"
CASE_TITLE = re.compile(rf"(?P<title>{PARTY_NAME}\s+v\.\s+{PARTY_NAME})\s*,?\s*$")


CITATION_PATTERNS: Tuple[Tuple[str, re.Pattern[str]], ...] = (
    ("statute", USC_CITATION),
    ("regulation", CFR_CITATION),
    ("rule", FED_RULE_CITATION),
    ("constitutional", CONSTITUTIONAL_CITATION),
    ("case_reporter", BASIC_CASE_CITATION),
)


def _reporter_from(raw: str) -> str:
    parts = raw.split()
    if len(parts) >= 3 and parts[0].isdigit() and parts[-1].isdigit():
        return " ".join(parts[1:-1])
    return ""


def _title_before(text: str, start: int) -> str | None:
    window = text[max(0, start - 120) : start]
    match = CASE_TITLE.search(window)
    if match:
        return match.group("title")
    return None


def _iter_citation_matches(text: str) -> Iterable[Tuple[str, re.Match[str]]]:
    seen_spans = set()
    for citation_type, pattern in CITATION_PATTERNS:
        for match in pattern.finditer(text):
            if match.span() in seen_spans:
                continue
            seen_spans.add(match.span())
            yield citation_type, match


def extract_citations(
    text: str,
    source_type: str = "web",
    retrieved_at: str = "",
    source_id: str | None = None,
    source_url: str | None = None,
) -> List[CitationObject]:
    citations = []
    matches = sorted(_iter_citation_matches(text), key=lambda item: item[1].start())
    for citation_type, match in matches:
        raw = match.group(0)
        reporter = _reporter_from(raw) if citation_type == "case_reporter" else None
        title = _title_before(text, match.start()) if citation_type == "case_reporter" else None
        citations.append(
            CitationObject(
                raw_text=raw,
                normalized_citation=" ".join(raw.split()),
                source_type=source_type,
                retrieved_at=retrieved_at,
                citation_type=citation_type,
                verification_status="unverified",
                authority_title=title,
                reporter=reporter,
                source_id=source_id,
                source_url=source_url,
                span_start=match.start(),
                span_end=match.end(),
                confidence=0.75,
                notes="Extracted citation; not legal verification.",
            )
        )
    return citations


def extract_basic_citations(text: str, source_type: str = "web", retrieved_at: str = "") -> List[CitationObject]:
    return [
        citation
        for citation in extract_citations(text, source_type=source_type, retrieved_at=retrieved_at)
        if citation.citation_type == "case_reporter"
    ]
