import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from omega_legal_citator.core.citation_parser import extract_basic_citations
from omega_legal_citator.core.pipeline import analyze_chat_export, analyze_legal_text


def main() -> None:
    parser = argparse.ArgumentParser(description="Omega-LegalCitator")
    parser.add_argument("text", nargs="?", help="Text to scan for legal citations")
    parser.add_argument("--chat-export", type=Path, help="Path to a ChatGPT-style JSON export to audit")
    parser.add_argument("--json", action="store_true", help="Emit full structured audit JSON")
    args = parser.parse_args()

    retrieved_at = datetime.now(UTC).isoformat()
    if args.chat_export:
        output = analyze_chat_export(
            json.loads(args.chat_export.read_text()),
            retrieved_at=retrieved_at,
            source_id=str(args.chat_export),
        )
    elif args.json:
        output = analyze_legal_text(args.text or "", retrieved_at=retrieved_at)
    else:
        results = extract_basic_citations(args.text or "", retrieved_at=retrieved_at)
        for item in results:
            print(item)
        return

    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
