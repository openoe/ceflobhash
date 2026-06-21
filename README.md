# ceflobhash

Binary vector representation & dual-node decision structure.
Designed with LLM embedding and neural representation efficiency in mind.

> `ceflobhash` = "Connect Everything Forever Low-Bit Hash"
> A lightweight take on how binary vectors can represent, compare, and verify high-dimensional LLM embeddings without floating-point math.

---

## Quick install

```bash
pip install ceflobhash
```

## What's in the box

```python
from root_boolean import (
    binarize,           # float vector → binary vector
    hamming_distance,   # binary vector distance
    DualNode,           # dual-node verification structure
)
```

Reducing 768-dimensional LLM embeddings to 256-bit binary vectors.
Hamming over cosine. No dot product. No softmax. Just bits.

## Examples

### 1. LLM embedding cache (binary lookup)

```python
from root_boolean import binarize, hamming_distance
import numpy as np

# Simulate LLM embedding cache
cache = {
    "dog": np.random.randn(768),
    "cat": np.random.randn(768),
    "car": np.random.randn(768),
}
query = np.random.randn(768)

# Binarize — no float ops, just bits
q_hm = binarize(query, bits=256)
results = sorted(
    (hamming_distance(q_hm, binarize(v, bits=256)), w)
    for w, v in cache.items()
)
```

### 2. State fingerprint (Conway's Game of Life)

```python
from root_boolean import binarize
board = [[0,1,0,0,0],[0,0,1,0,0],[1,1,1,0,0],
         [0,0,0,0,0],[0,0,0,0,0]]
vec = binarize([cell for row in board for cell in row], bits=64)
# Board fingerprint for state comparison
```

### 3. Dual-node verification (the part most people skip)

```python
from root_boolean import DualNode

node = DualNode(
    anchor_a=([1,0,1,0], (1,0,0,0), 3.0),
    anchor_b=([0,1,0,1], (0,1,0,0), 3.0),
)
v = node.evaluate(([1,0,1,0], (1,0,0,0)))
# → "TRUE" | "FALSE" | "UNKNOWN"
h = node.audit(([1,0,1,0], (1,0,0,0)), v)
# → SHA-256 fingerprint
```

## Why binary vectors for LLM work?

- **Memory**: 256 bits vs 768 float32 ≈ 96% less per embedding
- **Speed**: Hamming distance (XOR + popcount) vs dot product ≈ 10-50x faster
- **Verifiable**: DualNode produces an auditable fingerprint per decision

Not a replacement for attention. A complement for the parts that don't need it.

## Status

v0.1.1 — experimental. Works. Questions welcome.

---

MIT
