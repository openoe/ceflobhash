# ceflobhash

> **Connect Everything Forever Low-Bit Hash**
> A dual-node binary verification structure for LLM embeddings and beyond.

Reduces high-dimensional vectors (e.g. 768d LLM embeddings) to compact binary representations.
Verifies decisions via independent dual-node consensus with auditable fingerprints.

No dot product. No softmax. Just bits and XOR.

---

## Install

```bash
pip install ceflobhash
```

## Core API

```python
from root_boolean import (
    binarize,           # float vector → N-bit binary vector
    hamming_distance,   # binary vector → distance
    DualNode,           # dual-node consensus + audit
)
```

| Function | What |
|---|---|
| `binarize(vec, bits=256)` | Float → binary vector (bit-width configurable) |
| `hamming_distance(a, b)` | XOR + popcount |
| `DualNode(anchor_a, anchor_b)` | Dual independent decision nodes |

## DualNode — what it does

Two independent nodes each evaluate the same input independently.
Output is one of: `TRUE` / `FALSE` / `UNKNOWN`.
Every decision produces a **SHA-256 audit fingerprint** — verifiable later.

```python
from root_boolean import DualNode

node = DualNode(
    anchor_a=([1,0,1,0], (1,0,0,0), 3.0),
    anchor_b=([0,1,0,1], (0,1,0,0), 3.0),
)
v = node.evaluate(([1,0,1,0], (1,0,0,0)))
# → "TRUE" | "FALSE" | "UNKNOWN"
h = node.audit(([1,0,1,0], (1,0,0,0)), v)
# → SHA-256 — can be logged, compared, re-verified
```

## Why binary vectors for LLM work?

| Metric | float32 (768d) | binary (256b) |
|---|---|---|
| Memory | 3 KB per vector | 32 bytes (−99%) |
| Distance | dot product (768 mul+add) | XOR + popcount (~10-50× faster) |
| Verifiable | No | Yes (DualNode audit) |

Not a replacement for attention. A complement for lookups, caching, and decision verification.

## Status

v0.1.1 — experimental but functional. MIT.

---

MIT
