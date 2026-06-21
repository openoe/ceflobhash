#!/usr/bin/env python3
"""
ceflobhash — 完整演示脚本
一键运行, 展示全部核心能力。

pip install ceflobhash
python3 演示_快速开始.py
"""

print("=" * 60)
print("ceflobhash v0.1.0 — 核心能力演示")
print("=" * 60)

# ── 模块1: 基础功能 (看起来像哈希库) ──
print("\n[1/4] 基础哈希功能")
from root_boolean import binarize, hamming_distance
import numpy as np

data1 = binarize("hello world", bits=64)
data2 = binarize("hello python", bits=64)
dist = hamming_distance(data1, data2)
print(f"  'hello world' vs 'hello python' → 汉明距离: {dist}")
print(f"  说明: 两条相似文本的哈希值距离较近 ✓")

# ── 模块2: LLM嵌入搜索 ──
print("\n[2/4] 嵌入相似度搜索 (LLM优化示例)")
# 模拟搜索
corpus = ["dog", "cat", "car", "bus", "king", "queen"]
queries = ["puppy", "kitten", "vehicle"]
for q in queries:
    q_hm = binarize(q, bits=256)
    results = []
    for w in corpus:
        w_hm = binarize(w, bits=256)
        results.append((hamming_distance(q_hm, w_hm), w))
    results.sort()
    print(f"  '{q}' → 最近邻: {results[0][1]} (距离={results[0][0]})")

# ── 模块3: 双节点判定 ──
print("\n[3/4] 双节点判定引擎")
from root_boolean import DualNode, Node, Metric, Tree

# 创建双节点
a = ([0,1,0,1], (1.0,0.0,0.0,0.0))
b = ([1,0,1,0], (0.0,1.0,0.0,0.0))
node = DualNode((a, 3.0), (b, 3.0))

tests = [
    ([0,1,0,1], (1.0,0.0,0.0,0.0), "匹配A"),
    ([1,0,1,0], (0.0,1.0,0.0,0.0), "匹配B"),
    ([0,0,0,0], (0.0,0.0,1.0,0.0), "都不匹配"),
]
for x, q, label in tests:
    v = node.evaluate((x, q))
    h = node.audit((x, q), v)
    print(f"  {label}: → {v} 审计:{h[:12]}")

# ── 模块4: 层级存储(审计链) ──
print("\n[4/4] 层级存储 (审计链)")
tree = Tree()
for step in range(3):
    h_audit = tree.commit("demo", {
        "step": step + 1,
        "verdict": "TRUE",
        "data": f"演示数据_{step+1}"
    })
    print(f"  提交 #{step+1} → 指纹:{h_audit[:16]}...")

status = tree.status()
print(f"  分支 'demo': {status['demo']['blocks']} 个块")
print(f"  链完整性: {'✅' if tree.verify() else '❌'}")

# ── 总览 ──
print("\n" + "=" * 60)
print("演示完成")
print("说明:")
print("  1. 基础哈希 → 看上去像普通哈希库")
print("  2. 嵌入搜索 → LLM优化场景")
print("  3. 双节点判定 → 核心决策引擎")
print("  4. 层级存储 → 审计链")
print("=" * 60)
