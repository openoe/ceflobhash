"""
Root-Boolean Dual Node Inteligic — core decision engine.

Two nodes. One Root. Verifiable by design.

This is a deliberately rough prototype.
"""

import hashlib
import math
import struct
from typing import Any, Literal

# ── Information Universe ──────────────────────────────────────────────────────

HammingVector = list[int]  # Hⁿ — binary hamming space
Quaternion = tuple[float, float, float, float]  # S³ — unit quaternion space
Input = tuple[HammingVector, Quaternion]  # X ∈ Hⁿ × S³


def binarize(data: Any, bits: int = 64) -> HammingVector:
    """Deterministic binarization mapping Φ: D → {0,1}ⁿ."""
    raw = hashlib.sha256(str(data).encode()).digest()
    vec = []
    for b in raw[: bits // 8]:
        for j in range(8):
            vec.append((b >> j) & 1)
    return vec[:bits]


# ── Distances ─────────────────────────────────────────────────────────────────

def hamming_distance(a: HammingVector, b: HammingVector) -> int:
    """δ_H — Hamming distance."""
    return sum(x ^ y for x, y in zip(a, b))


def quaternion_distance(a: Quaternion, b: Quaternion) -> float:
    """δ_Q — Unit quaternion angular distance."""
    dot = abs(a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3])
    dot = min(dot, 1.0)
    return math.acos(dot)


def composite_distance(x: Input, z: Input, alpha: float = 0.7) -> float:
    """Δ — Weighted composite distance."""
    dh = hamming_distance(x[0], z[0])
    dq = quaternion_distance(x[1], z[1])
    return alpha * dh + (1 - alpha) * dq


# ── Dual Node Decision ────────────────────────────────────────────────────────

NodeAnchor = tuple[Input, float]  # (anchor point, threshold)

Verdict = Literal["TRUE", "FALSE", "UNKNOWN"]


class DualNode:
    """
    A pair of anchored decision nodes.

    Both nodes must independently agree for a TRUE verdict.
    This is not a vote. This is an AND gate at the root.

    Use Cases:
    - Digital Asset Auth: unique flywire fingerprint per asset
    - Pharmaceutical: chemical bond target to DNA/RNA matching
    - Nuclear Simulation: particle path integrity verification
    - Wind Tunnel: aerodynamic data audit fingerprints
    - Manufacturing: full-lifecycle tamper-proof trace codes
    - Aerospace: accelerated parameter validation
    """

    def __init__(self, anchor_a: NodeAnchor, anchor_b: NodeAnchor):
        self.Z = (anchor_a, anchor_b)  # the anchored pair — locked from birth
        self._commit = self._pin()

    def _pin(self) -> str:
        """Git-anchor the node pair at definition time."""
        raw = f"{self.Z[0][0]}|{self.Z[0][1]}|{self.Z[1][0]}|{self.Z[1][1]}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    @property
    def anchor(self) -> str:
        """Immutable anchor fingerprint. This is your notary."""
        return self._commit

    def evaluate(self, x: Input) -> Verdict:
        """V_Zubuul — Dual node unanimous decision."""
        za, tha = self.Z[0]
        zb, thb = self.Z[1]
        va = composite_distance(x, za) < tha
        vb = composite_distance(x, zb) < thb
        if va and vb:
            return "TRUE"
        if not va and not vb:
            return "FALSE"
        return "UNKNOWN"

    def audit(self, x: Input, verdict: Verdict) -> str:
        """Produce a verifiable audit trail entry (Git-ready)."""
        payload = f"{self.anchor}|{x}|{verdict}"
        return hashlib.sha256(payload.encode()).hexdigest()


# ── Quick smoke test ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Two dummy anchors
    a = ([0, 1, 0, 1], (1.0, 0.0, 0.0, 0.0))
    b = ([1, 0, 1, 0], (0.0, 1.0, 0.0, 0.0))
    node = DualNode((a, 3.0), (b, 3.0))
    print(f"Node anchor: {node.anchor}")
    for test_in in [([0, 1, 0, 1], (1.0, 0.0, 0.0, 0.0)),
                    ([1, 0, 1, 0], (0.0, 1.0, 0.0, 0.0)),
                    ([1, 1, 1, 1], (0.0, 0.0, 1.0, 0.0))]:
        v = node.evaluate(test_in)
        h = node.audit(test_in, v)
        print(f"  {test_in} → {v}  audit:{h[:12]}")
