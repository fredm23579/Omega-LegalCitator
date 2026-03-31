from omega_legal_citator.core.citation_parser import extract_basic_citations


def test_extract_basic_citations_finds_simple_pattern():
    text = "See 410 U.S. 113 and compare 347 U.S. 483."
    results = extract_basic_citations(text, retrieved_at="2026-03-31T00:00:00Z")
    assert len(results) >= 2
    assert results[0].raw_text == "410 U.S. 113"
