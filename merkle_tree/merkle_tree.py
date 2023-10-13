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
        ):
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

    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented

        return (
            (self.value, self.left, self.right, self.hash) ==
            (other.value, other.left, other.right, other.hash)
            )

    @property
    def hash(self) -> str:
        return self._hash.hexdigest()

    def __repr__(self):
        return f"{self.value}: {self.hash}"

class _NO_ROOT:
    
    def __str__(self):
        return "<Empty tree: Not root>"

    @property
    def value(self) -> NoReturn:
        raise AttributeError("Empty tree: root does not exist")
    
    @property
    def hash(self) -> NoReturn:
        raise AttributeError("Empty tree: root does not exist")


class MerkleTree:

    NO_ROOT = _NO_ROOT()

    def __init__(self, blocks: list[str]):
        self.blocks = blocks
        self.root = self.NO_ROOT
        self._build_tree([_MerkleNode(block) for block in self.blocks])

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
        return self._build_tree(parents)
