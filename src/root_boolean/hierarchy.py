"""
RBDN Hierarchy — 层级存储系统（MIT License）
================================

替代Git的GPL限制。纯Python, 零外部依赖, 全部MIT。

核心设计:
  - 内容寻址 (SHA-256, 同Git核心思想但独立实现)
  - 层级锚定 (区块→链→树)
  - 审计回溯 (任何历史状态可验证)
"""

import hashlib
import json
import time
from typing import Any, Optional


class Block:
    """最小存储单元: 一个判定结果 + 元数据"""
    __slots__ = ("data", "timestamp", "hash")

    def __init__(self, data: dict):
        self.data = data
        self.timestamp = time.time()
        self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        raw = json.dumps(self.data, sort_keys=True) + str(self.timestamp)
        return hashlib.sha256(raw.encode()).hexdigest()

    def verify(self) -> bool:
        return self.hash == self._compute_hash()


class Chain:
    """块链: Block → Block → Block  (单项链表, 每个块指向前一个)"""
    def __init__(self):
        self.blocks: list[Block] = []
        self._root = None

    def append(self, data: dict) -> str:
        block = Block(data)
        if self.blocks:
            data["_parent"] = self.blocks[-1].hash
        else:
            data["_parent"] = None
            self._root = block.hash
        block = Block(data)  # re-hash with parent
        self.blocks.append(block)
        return block.hash

    @property
    def tip(self) -> Optional[str]:
        return self.blocks[-1].hash if self.blocks else None

    @property
    def root(self) -> Optional[str]:
        return self._root

    def trace(self, from_idx: int = -1) -> list[dict]:
        """审计回溯: 从某个位置一路回到根"""
        result = []
        h = self.blocks[from_idx].hash if self.blocks else None
        for i in range(from_idx, -len(self.blocks) - 1, -1) if from_idx < 0 else range(from_idx, -1, -1):
            b = self.blocks[i]
            result.append({
                "hash": b.hash,
                "data": b.data,
                "ts": b.timestamp,
                "valid": b.verify(),
            })
            if b.data.get("_parent") is None:
                break
        return result

    def verify_chain(self) -> bool:
        """验证整条链的完整性"""
        prev = None
        for block in self.blocks:
            if not block.verify():
                return False
            if block.data["_parent"] != prev:
                return False
            prev = block.hash
        return True


class Tree:
    """层级树: 多链构成一个版本树"""
    def __init__(self):
        self.chains: dict[str, Chain] = {}
        self._meta: dict[str, dict] = {}

    def branch(self, name: str) -> Chain:
        """获取或创建分支"""
        if name not in self.chains:
            self.chains[name] = Chain()
            self._meta[name] = {"created": time.time(), "blocks": 0}
        return self.chains[name]

    def commit(self, branch: str, data: dict) -> str:
        """向分支追加一个判定"""
        self.branch(branch)  # 确保分支存在
        h = self.chains[branch].append(data)
        self._meta[branch]["blocks"] = len(self.chains[branch].blocks)
        self._meta[branch]["tip"] = h
        return h

    def status(self) -> dict:
        """树状态摘要"""
        return {
            branch: {
                "blocks": self._meta[branch]["blocks"],
                "tip": self._meta[branch].get("tip", "empty"),
            }
            for branch in self.chains
        }

    def export(self) -> str:
        """导出为可验证的JSON"""
        payload = {"meta": self._meta}
        for name, chain in self.chains.items():
            payload[name] = [
                {"hash": b.hash, "data": b.data, "ts": b.timestamp}
                for b in chain.blocks
            ]
        return json.dumps(payload, indent=2)

    @classmethod
    def import_(cls, payload: str) -> "Tree":
        """从JSON恢复"""
        t = cls()
        loaded = json.loads(payload)
        for name, blocks_data in loaded.items():
            if name == "meta":
                continue
            chain = t.branch(name)
            for bd in blocks_data:
                block = Block(bd["data"])
                block.timestamp = bd["ts"]
                block.hash = bd["hash"]
                chain.blocks.append(block)
        t._meta = loaded.get("meta", {})
        return t

    def verify(self) -> bool:
        """全树验证"""
        return all(c.verify_chain() for c in self.chains.values())


# ── 快速自检 ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("RBDN Hierarchy 自检")
    tree = Tree()

    h1 = tree.commit("main", {"verdict": "TRUE", "input": "king→queen", "step": 1})
    h2 = tree.commit("main", {"verdict": "TRUE", "input": "king→queen", "step": 2})
    h3 = tree.commit("dev", {"verdict": "UNKNOWN", "input": "dog→cat", "step": 1})

    print(f"  主链: {tree.status()['main']}")
    print(f"  dev链: {tree.status()['dev']}")
    print(f"  树验证: {'✅' if tree.verify() else '❌'}")
    print(f"  审计回溯:\n  {json.dumps(tree.chains['main'].trace(), indent=2)[:200]}")
    print("✅ MIT License — 零GPL依赖，自由使用")
