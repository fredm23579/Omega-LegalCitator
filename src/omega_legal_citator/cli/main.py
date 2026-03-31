import argparse
from datetime import datetime, UTC

from omega_legal_citator.core.citation_parser import extract_basic_citations


def main() -> None:
    parser = argparse.ArgumentParser(description="Omega-LegalCitator")
    parser.add_argument("text", help="Text to scan for legal citations")
    args = parser.parse_args()
    results = extract_basic_citations(args.text, retrieved_at=datetime.now(UTC).isoformat())
    for item in results:
        print(item)


if __name__ == "__main__":
    main()
