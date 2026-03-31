# Omega-LegalCitator

Omega-LegalCitator is a new open-source legal citator seed focused on citation extraction, normalization, provenance, and source-grounded authority resolution for public-interest legal technology.

## Initial goals
- Parse and normalize legal citations.
- Preserve provenance for every extracted authority.
- Support hybrid authority lookup across web, scholar-style literature discovery, cloud drives, social signals, Hugging Face resources, calendar-linked procedural context, and GitHub-hosted legal tooling.
- Keep a hard boundary between legal information support and legal advice.

## Planned source adapters
- Web
- Scholar
- GitHub
- Google Drive
- OneDrive
- Social
- Hugging Face
- Google Calendar

## Repository layout
- `docs/` architecture, roadmap, and source plans
- `src/omega_legal_citator/` Python package seed
- `tests/` starter tests
- `data/schemas/` canonical schema drafts

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Status
Seed repository scaffold with architecture and source-integration plan.
