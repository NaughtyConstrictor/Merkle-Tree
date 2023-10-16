from __future__ import annotations
from hashlib import sha256
from itertools import zip_longest
from typing import NoReturn
from queue import Queue

class _MerkleNode:
    
    def __init__(
        self, value: str | None = None, *, 
        left: _MerkleNode | None = None, 
        right: _MerkleNode | None = None
        ) -> None:
        if value is not None and not (left is None and right is None):
            raise ValueError("Can't provide both value and left or right")

        if right is None:
            right = left
        self.left = left
        self.right = right
        if value is None:
            self._hash = sha256(left._hash.digest() + right._hash.digest())
            value = left.value + right.value
        else:
            self._hash = sha256(value.encode("utf-8"))
            value = [value]
        self.value = value

    def __eq__(self, other: object) -> bool:
        if type(other) is not type(self):
            return NotImplemented

        return (
            (self.value, self.left, self.right, self.hash) ==
            (other.value, other.left, other.right, other.hash)
            )

    @property
    def hash(self) -> str:
        return self._hash.hexdigest()

    def __repr__(self) -> str:
        return f"{self.value}: {self.hash}"

class _NO_ROOT(_MerkleNode):
    
    def __init__(self) -> None:
        pass

    @property
    def left(self) -> NoReturn:
        raise AttributeError("Empty tree: root has no children")
    
    @property
    def right(self) -> NoReturn:
        raise AttributeError("Empty tree: root has no children")

    @property
    def value(self) -> NoReturn:
        raise AttributeError("Empty tree: root does not exist")
    
    @property
    def hash(self) -> NoReturn:
        raise AttributeError("Empty tree: root does not exist")

    def __str__(self) -> str:
        return "<Empty tree: Not root>"

    def __eq__(self, other: object) -> bool:
        if type(other) is type(self):
            return True
        return NotImplemented

class MerkleTree:

    NO_ROOT = _NO_ROOT()

    def __init__(self, blocks: list[str]) -> None:
        self.blocks = [sha256(block.encode("utf-8")).digest() for block in blocks]
        self.root = self.NO_ROOT
        self._levels = 0
        self._build_tree([_MerkleNode(block) for block in blocks])

    @property
    def nodes(self) -> list[list[_MerkleNode]]:
        if self.root is self.NO_ROOT:
            return None
        
        nodes = Queue()
        nodes.put(self.root)
        childs = []
        temp = []
        i = 0
        level_nodes = 1
        while not nodes.empty():
            i += 1
            node = nodes.get()
            temp.append(node)
            if i == level_nodes:
                childs.append(temp)
                temp = []
                i = 0
                level_nodes *= 2
            left, right = node.left, node.right
            if left:
                nodes.put(left)
            if right:
                nodes.put(right)
        
        return childs
    
    def _build_tree(self, children: list[_MerkleNode]) -> None:
        if len(children) == 0:
            return
        if len(children) == 1:
            self.root = children[0]
            return

        parents = []
        children = [iter(children)] * 2
        for left_child, right_child in zip_longest(*children):
            parent = _MerkleNode(left=left_child, right=right_child)
            parents.append(parent)
        self._levels += 1
        return self._build_tree(parents)

    def _index(self, value: str) -> int:
        try:
            return self.blocks.index(sha256(value.encode("utf-8")).digest())
        except ValueError:
            return -1
    
    def __contains__(self, value: str) -> bool:
        return bool(self._index(value) + 1)
    
    def proof(self, value: str, *, return_positions: bool = False
    )-> list[bytes] | tuple[list[bytes], list[int]]:
        position = self._index(value)
        if self._levels == 0 or position == -1:
            if return_positions:
                return [], []
            return []

        positions = bin(position)[2:].zfill(self._levels)
        path = []
        node = self.root
        for position in positions:
            if position == "1":
                path.append(node.left._hash.digest())
                node = node.right
            else:
                path.append(node.right._hash.digest())
                node = node.left
        
        path = path[::-1]
        if return_positions:
            positions = [int(position) for position in reversed(positions)]
            return path, positions
        return path
