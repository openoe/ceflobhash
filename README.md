# ceflobhash

> **Connect Everything Forever Low-Bit Hash**
> 连接永恒 · 低比特哈希

**Root-Boolean Dual Node Inteligic** — 一种可验证的双节点共识判定结构。
*A verifiable dual-node consensus decision structure.*

无点积、无Softmax、无概率。只有比特和XOR。
*No dot product. No softmax. No probability. Just bits and XOR.*

---

## 🇨🇳 中文说明

### 这是什么？

`ceflobhash` 将高维浮点向量（例如LLM的768维嵌入）压缩为紧凑的二进制表示，并通过**独立双节点共识**进行判定验证。每个判定产生可审计的指纹（SHA-256）。

### 核心理念

| 概念 | 说明 |
|---|---|
| **祖布尔双节点** | 节点A（字符匹配） + 节点B（语义类型匹配），独立判定 |
| **可审计指纹** | 每个决策输出 SHA-256 哈希，可事后重新验证 |
| **零概率** | 所有判定基于确定性门电路逻辑，非概率推理 |

### 安装

```bash
pip install ceflobhash
```

### 核心API

```python
from root_boolean import (
    binarize,           # float向量 → N位二进制向量
    hamming_distance,   # 二进制向量 → 汉明距离
    DualNode,           # 双节点共识 + 审计
)
```

| 函数 | 功能 |
|---|---|
| `binarize(vec, bits=256)` | 浮点向量 → 二进制向量（比特宽度可配） |
| `hamming_distance(a, b)` | XOR + 位计数 |
| `DualNode(anchor_a, anchor_b)` | 两个独立判定节点 |

### 双节点判定示例

```python
from root_boolean import DualNode

node = DualNode(
    anchor_a=([1,0,1,0], (1,0,0,0), 3.0),
    anchor_b=([0,1,0,1], (0,1,0,0), 3.0),
)
v = node.evaluate(([1,0,1,0], (1,0,0,0)))
# → "TRUE" | "FALSE" | "UNKNOWN"
h = node.audit(([1,0,1,0], (1,0,0,0)), v)
# → SHA-256 审计指纹
```

### 性能对比

| 指标 | float32 (768维) | binary (256位) |
|---|---|---|
| 内存 | 3 KB/向量 | 32 bytes (−99%) |
| 距离计算 | 点积 (768次乘加) | XOR + 位计数 (~10-50×更快) |
| 可验证 | ❌ | ✅ 双节点审计 |

不是替代注意力机制。而是为**检索、缓存、决策验证**提供补充。

---

## 🇬🇧 English

### What is this?

`ceflobhash` reduces high-dimensional float vectors (e.g. 768d LLM embeddings) to compact binary representations, and verifies decisions via **independent dual-node consensus**. Every decision produces an auditable SHA-256 fingerprint.

### Core Concepts

| Concept | Description |
|---|---|
| **Dual Node (Zubu'er)** | Node A (character match) + Node B (semantic type match), independently judge |
| **Auditable Fingerprint** | Each decision outputs SHA-256, re-verifiable later |
| **Zero Probability** | All decisions based on deterministic gate logic, not probabilistic |

### Install

```bash
pip install ceflobhash
```

### Core API

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

### DualNode Example

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

### Why Binary for LLM?

| Metric | float32 (768d) | binary (256b) |
|---|---|---|
| Memory | 3 KB per vector | 32 bytes (−99%) |
| Distance | dot product (768 mul+add) | XOR + popcount (~10-50× faster) |
| Verifiable | No | Yes (DualNode audit) |

Not a replacement for attention. A complement for lookups, caching, and decision verification.

---

## Use Cases / 应用方向

### 🇨🇳 中文

`ceflobhash` 的确定性门电路判定体系，可广泛应用于以下领域的**可验证身份、所有权确权与唯一性追溯**：

| 领域 | 应用 |
|---|---|
| **数字资产确权** | 每个数字资产生成唯一 SHA-256 飞线路径指纹，双节点判定验证所有权归属，不可伪造、不可抵赖 |
| **医药化学·关键靶点** | 化学键靶点（如蛋白质-配体结合位点）映射为确定性向量，双节点判定药物分子与DNA核酸序列的匹配度，可审计可复现 |
| **原子能模拟仿真** | 核反应过程中的粒子路径、能量分布模拟结果，通过双节点共识验证仿真数据的完整性与未被篡改性 |
| **风洞实验** | 风洞数据（气动参数/压力分布）生成不可逆的审计指纹，确保实验数据的真实性和可追溯性 |
| **制造业可追溯码** | 生产全生命周期（原料→加工→质检→出厂）每道工序生成唯一链式编码，双节点确保不可篡改 |
| **航空航天加速** | 研发计算中关键参数（轨道计算/结构强度分析）通过确定性判定加速验证流程，减少冗余校验 |

### 🇬🇧 English

The deterministic gate-circuit decision framework of `ceflobhash` enables **verifiable identity, ownership authentication, and unique traceability** across:

| Domain | Application |
|---|---|
| **Digital Asset Auth** | Each asset generates a unique SHA-256 flywire path fingerprint; dual-node consensus validates ownership — unforgeable, non-repudiable |
| **Pharmaceutical Target** | Map chemical bond targets (e.g. protein-ligand sites) to deterministic vectors; dual-node verifies drug molecule ↔ DNA/RNA sequence match — auditable & reproducible |
| **Nuclear Simulation** | Validate simulation integrity of particle paths and energy distribution in nuclear reactions via dual-node consensus, ensuring results remain untampered |
| **Wind Tunnel Testing** | Aerodynamic parameters and pressure distribution data generate irreversible audit fingerprints, guaranteeing authenticity and traceability |
| **Manufacturing Trace** | End-to-end lifecycle coding (material → fabrication → QC → shipment) via unique chained hashes per process step, dual-node verified against tampering |
| **Aerospace Acceleration** | Accelerate verification of critical parameters (orbit calculation, structural strength analysis) via deterministic gate decision, reducing redundant checks |

---

## Status / 状态

v0.1.3 — experimental but functional.
MIT License.

---

*CEF Powered — Connect Everything Forever*

> ceflobhash — 永恒连接之言
