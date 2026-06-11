from typing import Dict, Iterable, List, Tuple

from omega_legal_citator.models.framework_stack import FrameworkStackClassification


STACK_SIGNALS: Dict[str, Tuple[str, Iterable[str]]] = {
    "structural_impossibility": (
        "Structural impossibility / institutional-capacity challenge",
        ("impossible", "impossibility", "institutional capacity", "cannot comply", "structural"),
    ),
    "standing": (
        "Article III standing / injury traceability redressability",
        ("standing", "injury in fact", "traceability", "redressability"),
    ),
    "equitable_relief": (
        "Equitable relief / injunction framework",
        ("injunction", "irreparable harm", "balance of equities", "public interest"),
    ),
    "jurisdiction": (
        "Jurisdiction / procedural threshold",
        ("jurisdiction", "venue", "ripeness", "mootness"),
    ),
}


def classify_framework_stack(text: str) -> List[FrameworkStackClassification]:
    lowered = text.lower()
    classifications: List[FrameworkStackClassification] = []
    for stack_id, (label, signals) in STACK_SIGNALS.items():
        matched = [signal for signal in signals if signal in lowered]
        if matched:
            confidence = min(0.9, 0.45 + (0.15 * len(matched)))
            classifications.append(
                FrameworkStackClassification(
                    stack_id=stack_id,
                    label=label,
                    confidence=confidence,
                    signals=matched,
                    verification_status="unverified",
                )
            )
    return classifications
