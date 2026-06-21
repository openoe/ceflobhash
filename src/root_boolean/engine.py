"""
RBDN Engine — 完整判定引擎 v1.0
包含: Hⁿ·S³空间映射, 双节点判定, 验证函数族, 加权共识, 状态转移, 偏差定位, 修正迭代, Git审计
"""

import hashlib, math, numpy as np
from typing import Any, Literal

Verdict = Literal["TRUE", "FALSE", "UNKNOWN"]

# ── 度量层 ─────────────────────────────────────────────────────────────────

class Metric:
    """复合度量: δ_H + δ_Q"""
    @staticmethod
    def hamming(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.sum(a != b)) / max(len(a), 1)

    @staticmethod
    def quaternion(p: tuple, q: tuple) -> float:
        dot = abs(p[0]*q[0] + p[1]*q[1] + p[2]*q[2] + p[3]*q[3])
        return math.acos(min(dot, 1.0)) / math.pi  # 归一化到[0,1]

    @staticmethod
    def composite(x_hm, z_hm, x_q, z_q, alpha=0.6) -> float:
        dh = Metric.hamming(x_hm, z_hm)
        dq = Metric.quaternion(x_q, z_q)
        return alpha * dh + (1 - alpha) * dq

    @staticmethod
    def jaccard(a: np.ndarray, b: np.ndarray) -> float:
        inter = float(np.sum((a > 0) & (b > 0)))
        union = float(np.sum((a > 0) | (b > 0)))
        return 1 - inter / max(union, 1)

    @staticmethod
    def edit_distance(a: np.ndarray, b: np.ndarray) -> float:
        """归一化编辑距离"""
        diff = np.sum(a != b)
        return diff / max(len(a), 1)

# ── 验证函数族 ─────────────────────────────────────────────────────────────

class Verifier:
    def __init__(self, name: str, metric_fn, threshold: float, weight: float = 1.0):
        self.name = name
        self.fn = metric_fn
        self.theta = threshold
        self.w = weight

    def verify(self, x, z) -> bool:
        return self.fn(x, z) < self.theta

# ── 节点 ────────────────────────────────────────────────────────────────────

class Node:
    """带多验证器的锚点节点"""
    def __init__(self, hamming_vec, quat=(1,0,0,0), threshold=0.35):
        self.h = hamming_vec.astype(int) if isinstance(hamming_vec, np.ndarray) else np.array(hamming_vec)
        self.q = np.array(quat, dtype=float)
        self.theta = threshold
        self.verifiers = [
            Verifier("hamming", Metric.hamming, threshold, 1.0),
            Verifier("jaccard", Metric.jaccard, 0.8, 0.7),
            Verifier("edit", Metric.edit_distance, threshold, 0.9),
        ]
        self.pin = hashlib.sha256(self.h.tobytes() + self.q.tobytes()).hexdigest()[:16]

    def evaluate(self, x_hm, x_q) -> tuple[Verdict, dict, float]:
        """多验证器加权判定"""
        results = {}
        total_weight = 0
        agree_weight = 0
        for v in self.verifiers:
            ok = v.verify(x_hm if "hamming" in v.name or "edit" in v.name or "jaccard" in v.name else x_hm, self.h)
            results[v.name] = ok
            total_weight += v.w
            if ok:
                agree_weight += v.w

        # 加权共识阈值51%
        consensus = agree_weight / max(total_weight, 1)
        if consensus >= 0.51:
            verdict: Verdict = "TRUE"
        elif consensus <= 0.3:
            verdict: Verdict = "FALSE"
        else:
            verdict: Verdict = "UNKNOWN"
        return verdict, results, consensus

# ── 锚定层 ──────────────────────────────────────────────────────────────────

class Audit:
    def __init__(self):
        self.chain = []

    def commit(self, label: str, data: dict) -> str:
        payload = f"{label}|{sorted(data.items())}"
        h = hashlib.sha256(payload.encode()).hexdigest()[:16]
        self.chain.append({"label": label, "hash": h, "data": data})
        return h

# ── 偏差定位 ────────────────────────────────────────────────────────────────

class Deviation:
    @staticmethod
    def locate(x_hm, z_hm) -> list[int]:
        """D(x,Z) — 定位哪些比特导致偏差"""
        return [i for i in range(min(len(x_hm), len(z_hm))) if x_hm[i] != z_hm[i]]

    @staticmethod
    def correct(x_hm, z_hm, lam=0.5) -> np.ndarray:
        """∇修正: 将x向锚点方向拉"""
        x2 = x_hm.copy().astype(float)
        diff = Deviation.locate(x_hm, z_hm)
        for i in diff:
            x2[i] += lam * (1 if z_hm[i] > 0 else -1)
        # 重新二值化
        return (x2 > 0.5).astype(int)

# ── 状态转移 ────────────────────────────────────────────────────────────────

class StateTransition:
    def __init__(self, max_steps=5):
        self.max_steps = max_steps

    def run(self, nodes: list[Node], x_hm, x_q, audit: Audit) -> dict:
        """完整的链式迭代判定"""
        step = 0
        verdict: Verdict = "UNKNOWN"
        current_x = x_hm.copy()

        while step < self.max_steps and verdict != "TRUE":
            step += 1
            node_results = {}
            for i, node in enumerate(nodes):
                v, details, consensus = node.evaluate(current_x, x_q)
                node_results[f"node_{i}"] = {"verdict": v, "consensus": f"{consensus:.2f}"}

            # 多节点AND共识
            all_true = all(r["verdict"] == "TRUE" for r in node_results.values())
            verdict = "TRUE" if all_true else ("FALSE" if not any(r["verdict"] == "TRUE" for r in node_results.values()) else "UNKNOWN")

            audit.commit(f"step_{step}", {"verdict": verdict, **node_results})

            # 如果未通过: 偏差定位+修正
            if verdict != "TRUE":
                for node in nodes:
                    diff = Deviation.locate(current_x, node.h)
                    if diff:
                        current_x = Deviation.correct(current_x, node.h, lam=0.3)

        return {
            "verdict": verdict,
            "steps": step,
            "final_x": current_x,
            "audit_chain": audit.chain[-step:] if audit.chain else []
        }
