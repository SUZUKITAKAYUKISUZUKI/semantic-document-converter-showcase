> Illustrative expected output for the synthetic source.

# Signal Ledger

## A Synthetic Document Processing Example

A reliable converter preserves what the page says, keeps structural relationships visible, and marks uncertain evidence for review instead of inventing a convenient answer.

### Routing Example

```python
def route(item):
    if item.kind == "diagram":
        return "visual"
    return "text"
```

### Evidence Flow

```mermaid
flowchart LR
    A[Capture] --> B[Normalize]
    B --> C[Verify]
```

### Review Score

A compact review score combines confirmed content `c`, structural matches `s`, and unresolved items `u`:

$$
Q = \frac{c + s}{1 + u}
$$
