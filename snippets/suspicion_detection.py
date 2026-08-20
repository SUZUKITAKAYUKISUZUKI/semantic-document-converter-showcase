"""
Representative simplified example for portfolio purposes.
The production implementation remains private.
"""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Suspicion:
    category: str
    excerpt: str


def scan(text: str) -> list[Suspicion]:
    """Flag evidence for review without changing the supplied text."""
    findings: list[Suspicion] = []

    repeated = re.search(r"(.)\1{5,}", text)
    if repeated:
        findings.append(Suspicion("abnormal_repetition", repeated.group(0)))

    broken_link = re.search(r"https?://\S+\s+/\s*\S+", text)
    if broken_link:
        findings.append(Suspicion("broken_url_like_text", broken_link.group(0)))

    markup_is_unbalanced = text.count("<") != text.count(">")
    noisy_markup = re.search(r"[<>{}]{4,}", text)
    if markup_is_unbalanced or noisy_markup:
        excerpt = noisy_markup.group(0) if noisy_markup else text[:40]
        findings.append(Suspicion("markup_suspicion", excerpt))

    return findings


if __name__ == "__main__":
    sample = "Read https://example.test /guide before <<<< continuing."
    for suspicion in scan(sample):
        print(f"{suspicion.category}: {suspicion.excerpt}")
