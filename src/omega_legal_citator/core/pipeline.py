from omega_legal_citator.core.citation_audit import audit_citations
from omega_legal_citator.core.citation_parser import extract_citations
from omega_legal_citator.core.framework_stack import classify_framework_stack
from omega_legal_citator.models.authority_graph import AuthorityGraph


def analyze_legal_text(
    text: str,
    source_type: str = "web",
    retrieved_at: str = "",
    source_id: str | None = None,
    source_url: str | None = None,
) -> dict:
    citations = extract_citations(
        text,
        source_type=source_type,
        retrieved_at=retrieved_at,
        source_id=source_id,
        source_url=source_url,
    )
    graph = AuthorityGraph.from_citations(citations)
    audit = audit_citations(text, citations)
    stacks = classify_framework_stack(text)
    return {
        "citations": [citation.__dict__ for citation in citations],
        "authority_graph": graph.to_dict(),
        "framework_stacks": [stack.__dict__ for stack in stacks],
        "audit": audit.to_dict(),
        "legal_advice": False,
        "verification_status": "unverified",
    }

def _message_text(message: dict) -> str:
    content = message.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(str(item.get("text", "")) for item in content if isinstance(item, dict))
    if isinstance(content, dict):
        if isinstance(content.get("parts"), list):
            return "\n".join(str(part) for part in content["parts"] if part is not None)
        return str(content.get("text", ""))
    return ""


def _chat_messages(chat_export: dict) -> list[dict]:
    if isinstance(chat_export.get("messages"), list):
        return chat_export["messages"]
    if isinstance(chat_export.get("mapping"), dict):
        messages = []
        for node in chat_export["mapping"].values():
            message = node.get("message") if isinstance(node, dict) else None
            if isinstance(message, dict):
                messages.append(message)
        return messages
    return []


def analyze_chat_export(
    chat_export: dict,
    retrieved_at: str = "",
    source_id: str | None = None,
    source_url: str | None = None,
) -> dict:
    """Analyze a minimal ChatGPT-style export without claiming legal verification."""
    segments = []
    for index, message in enumerate(_chat_messages(chat_export), start=1):
        text = _message_text(message)
        if text.strip():
            role = message.get("role") or message.get("author", {}).get("role") or "unknown"
            segments.append(f"[message:{index}; role:{role}]\n{text}")

    conversation_id = source_id or chat_export.get("id") or chat_export.get("conversation_id")
    return analyze_legal_text(
        "\n\n".join(segments),
        source_type="chat_export",
        retrieved_at=retrieved_at,
        source_id=conversation_id,
        source_url=source_url,
    )

