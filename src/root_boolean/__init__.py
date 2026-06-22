"""
Root-Boolean Dual Node Inteligic (MIT License)

Two nodes. One Root. Verifiable by design.

ceflobhash — Connect Everything Forever Low-Bit Hash
确定性门电路判定体系 | Deterministic Gate-Circuit Decision Framework

应用方向 / Use Cases:
- 数字资产确权 / Digital Asset Authentication
- 医药化学键·DNA核酸匹配 / Pharmaceutical Target & DNA/RNA Matching
- 原子能模拟仿真 / Nuclear Simulation Verification
- 风洞实验追溯 / Wind Tunnel Data Traceability
- 制造业全链可追溯码 / Manufacturing Full-Lifecycle Trace Code
- 航空航天研发计算加速 / Aerospace R&D Computation Acceleration
"""

from .core import DualNode, binarize, composite_distance, hamming_distance
from .engine import Node, Metric, Audit, StateTransition, Deviation, Verifier
from .hierarchy import Block, Chain, Tree

__all__ = [
    "DualNode", "binarize", "composite_distance", "hamming_distance",
    "Node", "Metric", "Audit", "StateTransition", "Deviation", "Verifier",
    "Block", "Chain", "Tree",
]
