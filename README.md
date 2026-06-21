# Root-Boolean

Some hash-like utilities for binary vector operations.
Built on a decision structure with two independent nodes.

---

## Quick install

```bash
pip install ceflobhash
```

## What's in the box

```python
from root_boolean import (
    binarize,      # float → binary vector
    hamming_distance,  # binary vector distance
)
```

A couple of hash-adjacent tools.
Nothing groundbreaking.

## Examples

### 1. Quick embedding search (LLM optimization snippet)

```python
from root_boolean import binarize, hamming_distance
import numpy as np

# Simulate a small embedding cache
cache = {
    "dog": np.random.randn(768),
    "cat": np.random.randn(768),
    "car": np.random.randn(768),
}
query = np.random.randn(768)

# Binarize everything
q_hm = binarize(query, bits=256)
results = []
for word, vec in cache.items():
    v_hm = binarize(vec, bits=256)
    d = hamming_distance(q_hm, v_hm)
    results.append((d, word))
results.sort()
# → nearest neighbor by Hamming, no dot product needed
```

### 2. Conway's Game of Life (state cell demo)

```python
from root_boolean import binarize

# Encode a 5x5 Game of Life board as a binary vector
board = [
    [0,1,0,0,0],
    [0,0,1,0,0],
    [1,1,1,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
]
flat = [cell for row in board for cell in row]
# Pad to 64 bits and hash
vec = binarize(flat, bits=64)
# → can be used as a "board fingerprint" for state comparison
```

### 3. Dual node check (the part nobody asked for)

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

## Status

v0.1.0 — casual release. Issues and comments welcome.

---

MIT
