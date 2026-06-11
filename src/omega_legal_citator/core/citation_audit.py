import re
from typing import Iterable, List

from omega_legal_citator.models.audit import CitationAuditFinding, CitationAuditReport
from omega_legal_citator.models.citation import CitationObject


KNOWN_AUTHORITY_CITATIONS = {
    "Brown v. Board of Education": "347 U.S. 483",
    "Marbury v. Madison": "5 U.S. 137",
    "Roe v. Wade": "410 U.S. 113",
    "Ashcroft v. Iqbal": "556 U.S. 662",
}


TITLE_WORD = r"[A-Z][A-Za-z0-9.'&-]+"
TITLE_CONNECTOR = r"(?:of|the|and|for|in|on|to|by|from|with|as|at|de|del|la|le|van|von)"
PARTY_NAME = rf"{TITLE_WORD}(?:\s+(?:{TITLE_CONNECTOR}\s+)?{TITLE_WORD})*"


TITLE_WITH_CITATION = re.compile(
    rf"(?P<title>{PARTY_NAME}\s+v\.\s+{PARTY_NAME})\s*,?\s+"
    r"(?P<citation>\d+\s+[A-Z][A-Za-z.0-9]*\s+\d+)"
)


def _suspected_miscitation_findings(text: str) -> Iterable[CitationAuditFinding]:
    for index, match in enumerate(TITLE_WITH_CITATION.finditer(text), start=1):
        title = match.group("title")
        citation = match.group("citation")
        expected = KNOWN_AUTHORITY_CITATIONS.get(title)
        if expected and expected != citation:
            yield CitationAuditFinding(
                finding_id=f"blocker:mis-citation:{index}",
                severity="blocker",
                category="suspected_mis_citation",
                message="Known authority title is paired with a different seed citation.",
                citation=citation,
                authority_title=title,
                expected_citation=expected,
                blocks_release=True,
            )


def audit_citations(text: str, citations: List[CitationObject]) -> CitationAuditReport:
    findings: List[CitationAuditFinding] = list(_suspected_miscitation_findings(text))
    for index, citation in enumerate(citations, start=1):
        if citation.verification_status != "verified":
            findings.append(
                CitationAuditFinding(
                    finding_id=f"info:unverified:{index}",
                    severity="info",
                    category="unverified_extraction",
                    message="Citation was extracted but has not been source-verified or citator-checked.",
                    citation=citation.normalized_citation,
                    authority_title=citation.authority_title,
                    blocks_release=False,
                )
            )
    return CitationAuditReport(findings=findings)
