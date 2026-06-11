from omega_legal_citator.core.citation_audit import audit_citations
from omega_legal_citator.core.citation_parser import extract_citations
from omega_legal_citator.core.framework_stack import classify_framework_stack
from omega_legal_citator.core.pipeline import analyze_chat_export, analyze_legal_text
from omega_legal_citator.models.authority_graph import AuthorityGraph


def test_extract_citations_finds_multiple_authority_types():
    text = (
        "Roe v. Wade, 410 U.S. 113 discusses constitutional questions. "
        "See also 42 U.S.C. § 1983, 28 C.F.R. § 35.130, "
        "Fed. R. Civ. P. 65, and U.S. Const. amend. XIV."
    )
    results = extract_citations(text, retrieved_at="2026-06-11T00:00:00Z")
    citation_types = {result.citation_type for result in results}

    assert {"case_reporter", "statute", "regulation", "rule", "constitutional"} <= citation_types
    assert all(result.verification_status == "unverified" for result in results)


def test_authority_graph_preserves_unverified_provenance():
    citations = extract_citations(
        "Brown v. Board of Education, 347 U.S. 483",
        source_type="chat_export",
        retrieved_at="2026-06-11T00:00:00Z",
        source_id="chat-1",
    )
    graph = AuthorityGraph.from_citations(citations)
    authority = next(iter(graph.authorities.values()))

    assert authority.verification_status == "unverified"
    assert authority.provenance[0].source_type == "chat_export"
    assert authority.provenance[0].source_id == "chat-1"


def test_miscitation_becomes_blocker_finding():
    text = "Brown v. Board of Education, 410 U.S. 113"
    citations = extract_citations(text, retrieved_at="2026-06-11T00:00:00Z")
    report = audit_citations(text, citations)

    assert citations[0].authority_title == "Brown v. Board of Education"
    assert report.has_blockers is True
    blocker = next(finding for finding in report.findings if finding.blocks_release)
    assert blocker.category == "suspected_mis_citation"
    assert blocker.expected_citation == "347 U.S. 483"


def test_framework_stack_classification_is_structured_not_advice():
    stacks = classify_framework_stack(
        "The remedy demand raises structural impossibility and institutional capacity concerns."
    )

    assert stacks[0].stack_id == "structural_impossibility"
    assert stacks[0].verification_status == "unverified"


def test_pipeline_outputs_audit_objects_not_legal_advice():
    output = analyze_legal_text(
        "A possible injunction theory cites Fed. R. Civ. P. 65 and 410 U.S. 113.",
        source_type="chat_export",
        retrieved_at="2026-06-11T00:00:00Z",
    )

    assert output["legal_advice"] is False
    assert output["verification_status"] == "unverified"
    assert output["audit"]["findings"]
    assert output["authority_graph"]["authorities"]

def test_chat_export_pipeline_reads_content_parts_and_preserves_governance():
    export = {
        "id": "conversation-1",
        "mapping": {
            "node-1": {
                "message": {
                    "author": {"role": "assistant"},
                    "content": {
                        "content_type": "text",
                        "parts": ["Brown v. Board of Education, 410 U.S. 113"],
                    },
                }
            }
        },
    }

    output = analyze_chat_export(export, retrieved_at="2026-06-11T00:00:00Z")

    assert output["legal_advice"] is False
    assert output["verification_status"] == "unverified"
    assert output["citations"][0]["source_type"] == "chat_export"
    assert output["citations"][0]["source_id"] == "conversation-1"
    assert output["audit"]["has_blockers"] is True
