"""String utility functions."""

from __future__ import annotations


def sanitize_name(name: str, allow_hyphen: bool = True) -> str:
    """Sanitize a name for URDF and Python identifier compatibility.

    Replaces invalid characters with underscores and ensures it doesn't
    start with a digit.

    Args:
        name: Original name
        allow_hyphen: Whether to allow hyphens (valid in URDF, invalid in Python)

    Returns:
        Sanitized name
    """
    if not name:
        return ""

    # Prevent ReDoS: limit input length before processing
    if len(name) > 1000:
        raise ValueError(f"Name too long: {len(name)} characters (maximum 1000)")

    # Replace spaces with underscores
    name = name.replace(" ", "_")

    # Character iteration (safer than regex)
    allowed_special = ("_", "-") if allow_hyphen else ("_",)
    sanitized = "".join(c if c.isalnum() or c in allowed_special else "_" for c in name)

    # Ensure it doesn't start with a digit
    if sanitized and sanitized[0].isdigit():
        sanitized = f"_{sanitized}"

    return sanitized
