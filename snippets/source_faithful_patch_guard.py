"""
Representative simplified example for portfolio purposes.
The production implementation remains private.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CandidatePatch:
    expected: str
    replacement: str
    source_verified: bool


@dataclass(frozen=True)
class PatchDecision:
    accepted: bool
    text: str
    reason: str


def apply_if_safe(current: str, patch: CandidatePatch) -> PatchDecision:
    """Accept one narrow replacement only when deterministic checks pass."""
    if not patch.source_verified:
        return PatchDecision(False, current, "source evidence was not verified")

    if not patch.expected or current.count(patch.expected) != 1:
        return PatchDecision(False, current, "target is missing or ambiguous")

    size_change = len(patch.replacement) - len(patch.expected)
    if abs(size_change) > 1:
        return PatchDecision(False, current, "edit exceeds the local size boundary")

    if "\n" in patch.expected or "\n" in patch.replacement:
        return PatchDecision(False, current, "multi-line rewrite is outside this guard")

    updated = current.replace(patch.expected, patch.replacement, 1)
    return PatchDecision(True, updated, "accepted source-backed local correction")


if __name__ == "__main__":
    proposal = CandidatePatch("modem", "model", source_verified=True)
    decision = apply_if_safe("Use the local modem.", proposal)
    print(decision)
