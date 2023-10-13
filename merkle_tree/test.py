from abc import ABC, abstractclassmethod
from merkle_tree import MerkleTree
from merkle_tree.merkle_tree import _MerkleNode
import unittest

EMPTY_LIST = []
SINGLE_ITEM_LIST = ["ahmed"]
ODD_LENGTH_LIST = ["ahmed", "amine", "yousa"]
EVEN_LENGTH_LIST = ["ahmed", "amine", "yousa", "sara"]


class TestMerkleTree(ABC):

    root = None
    nodes = None

    @abstractclassmethod
    def setUpClass(cls):
        pass

    def test_root_value(self):
        self.assertEqual(self.tree.root.value, self.root.value)

    def test_root_hash(self):
        self.assertEqual(self.tree.root.hash, self.root.hash)
    
    def test_nodes(self):
        self.assertListEqual(self.tree.nodes, self.nodes)

class TestEmptyMerkleTree(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tree = MerkleTree(EMPTY_LIST)

    def test_empty_tree_root(self):
        self.assertIs(self.tree.root, MerkleTree.NO_ROOT)
    
    def test_empty_tree_root_value(self):
        with self.assertRaisesRegex(AttributeError, "Empty tree: root does not exist"):
            self.tree.root.value

    def test_empty_tree_root_hash(self):
        with self.assertRaisesRegex(AttributeError, "Empty tree: root does not exist"):
            self.tree.root.hash
    
    def test_empty_tree_nodes(self):
        self.assertIs(self.tree.nodes, None)


class TestMerkleTreeSingle(TestMerkleTree, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tree = MerkleTree(SINGLE_ITEM_LIST)
        cls.root = _MerkleNode(SINGLE_ITEM_LIST[0])
        cls.nodes = [[cls.root]]

class TestMerkleTreeOdd(TestMerkleTree, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tree = MerkleTree(ODD_LENGTH_LIST)
        A, B, C = [_MerkleNode(item) for item in ODD_LENGTH_LIST]
        AB, CC = _MerkleNode(left=A, right=B), _MerkleNode(left=C)
        ABCC = _MerkleNode(left=AB, right=CC) 
        cls.root = ABCC
        cls.nodes = [[ABCC], [AB, CC], [A, B, C, C]]


class TestMerkleTreeEven(TestMerkleTree, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tree = MerkleTree(EVEN_LENGTH_LIST)
        A, B, C, D = [_MerkleNode(item) for item in EVEN_LENGTH_LIST]
        AB, CD = _MerkleNode(left=A, right=B), _MerkleNode(left=C, right=D)
        ABCD = _MerkleNode(left=AB, right=CD) 
        cls.root = ABCD
        cls.nodes = [[ABCD], [AB, CD], [A, B, C, D]]

