import re


def _amount(pattern: str, text: str, default: float) -> float:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return default
    return float(match.group(1).replace(",", ""))


def parse_policy(policy: str) -> dict:
    """Turn the supported plain-English policy format into rule settings."""
    text = " ".join(policy.strip().split())

    department_match = re.search(
        r"(?:for|within)\s+([A-Za-z][A-Za-z &/-]*?)"
        r"(?=\s*(?:,|;|\band\b|\bunder\b|\bbelow\b|\bup to\b|$))",
        text,
        flags=re.IGNORECASE,
    )
    department = department_match.group(1).strip() if department_match else "Sales"
    department = re.sub(
        r"\s+(?:expenses?|claims?)$",
        "",
        department,
        flags=re.IGNORECASE,
    )

    auto_approve_below = _amount(
        r"(?:under|below|less than|up to)\s*\$?\s*([\d,]+(?:\.\d+)?)",
        text,
        500,
    )

    escalate_above = _amount(
        r"(?:escalat\w*|escalation).{0,60}?"
        r"(?:above|over|exceed\w*)\s*\$?\s*([\d,]+(?:\.\d+)?)",
        text,
        2000,
    )
    if escalate_above == 2000:
        escalate_above = _amount(
            r"escalat\w*\s+(?:expenses?\s+)?(?:above|over)\s*"
            r"\$?\s*([\d,]+(?:\.\d+)?)",
            text,
            2000,
        )

    reject_above = _amount(
        r"(?:reject|rejection).{0,60}?"
        r"(?:above|over|exceed\w*)\s*\$?\s*([\d,]+(?:\.\d+)?)",
        text,
        5000,
    )
    if reject_above == 5000:
        reject_above = _amount(
            r"reject\s+(?:expenses?\s+)?(?:above|over)\s*"
            r"\$?\s*([\d,]+(?:\.\d+)?)",
            text,
            5000,
        )

    return {
        "auto_approve_department": department,
        "auto_approve_below": auto_approve_below,
        "escalate_above": escalate_above,
        "reject_above": reject_above,
    }
