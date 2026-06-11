# ADR-001: Legal Information Infrastructure Boundary

## Status

Accepted

## Context

Omega-LegalCitator is a legal reasoning infrastructure layer. The first durable version must extract, normalize, classify, provenance-lock, verify, score, audit, and generate structured outputs that another system can use. It must not act as an autonomous legal answer generator.

## Decision

All extracted authorities start as `unverified`. Extraction does not imply source verification, citator treatment, proposition fit, or legal sufficiency. The system may produce structured citation, authority graph, framework-stack, provenance, and audit objects. It must not produce filing-ready legal conclusions or represent outputs as legal advice.

Suspected mis-citations are blocker findings. A blocker finding means downstream release or reliance should stop until a human or trusted resolver verifies the authority, citation, source text, and proposition fit.

## Consequences

- Legal advice generation remains out of scope.
- Structured outputs are designed for traceability, challenge, correction, and versioning.
- Resolvers such as CourtListener, CAP, or official-source adapters can later upgrade authority status.
- Agent-Omega can govern future upgrades through mutation lifecycle, judge, archivist, and deployment rails.
