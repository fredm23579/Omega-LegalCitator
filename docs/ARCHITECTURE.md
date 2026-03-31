# Architecture

## Core thesis
Omega-LegalCitator should separate:
1. Citation and authority extraction
2. Normalization and provenance tracking
3. Retrieval and source adapters
4. Confidence and governance checks
5. Export surfaces for research, review, and downstream formalization

## Proposed modules
- `core/citation_parser.py`
  - Extract citations from text
  - Detect reporter patterns and basic citation spans
- `core/normalizer.py`
  - Normalize courts, reporters, and citation strings
- `core/provenance.py`
  - Attach source, timestamp, document identity, and confidence metadata
- `core/resolver.py`
  - Resolve a citation into candidate authorities
- `connectors/`
  - Source adapters for each requested source family
- `models/`
  - Typed models for citation objects and authority objects
- `cli/`
  - Simple command-line entry points

## Source families
- Web: public legal sites, court sites, and open repositories
- Scholar: research and academic discovery layer for legal scholarship
- GitHub: open-source legal tooling and datasets
- Google Drive: user documents and exported corpora
- OneDrive: user documents and exported corpora
- Social: public legal-policy and court-adjacent signals
- Hugging Face: models, datasets, and spaces relevant to legal citation and retrieval
- Google Calendar: deadlines, hearings, and procedural event context

## Governance
- Never present strategy as legal advice.
- Preserve provenance on every extracted authority.
- Mark unresolved citations and ambiguous matches explicitly.
- Keep retrieval and reasoning layers auditable.
