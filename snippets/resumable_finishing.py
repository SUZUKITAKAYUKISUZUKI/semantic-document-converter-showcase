"""
Representative simplified example for portfolio purposes.
The production implementation remains private.
"""

from collections.abc import Callable, Iterable
import json
import os
from pathlib import Path


def load_completed(checkpoint: Path) -> dict[str, str]:
    if not checkpoint.exists():
        return {}
    payload = json.loads(checkpoint.read_text(encoding="utf-8"))
    return dict(payload.get("completed", {}))


def save_completed(checkpoint: Path, completed: dict[str, str]) -> None:
    temporary = checkpoint.with_suffix(".tmp")
    payload = {"completed": completed}
    temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    os.replace(temporary, checkpoint)


def finish_chunks(
    chunks: Iterable[tuple[str, str]],
    checkpoint: Path,
    finish_one: Callable[[str], str],
) -> list[str]:
    """Resume at the first incomplete chunk and preserve stable ordering."""
    ordered_chunks = list(chunks)
    completed = load_completed(checkpoint)

    for chunk_id, content in ordered_chunks:
        if chunk_id in completed:
            continue

        result = finish_one(content)
        completed[chunk_id] = result
        save_completed(checkpoint, completed)

    return [completed[chunk_id] for chunk_id, _ in ordered_chunks]


if __name__ == "__main__":
    work = [("chunk-1", "alpha"), ("chunk-2", "beta")]
    output = finish_chunks(work, Path("checkpoint.json"), str.upper)
    print(output)
