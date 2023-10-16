from abc import ABC, abstractclassmethod
from functools import reduce
from hashlib import sha256
from merkle_tree import MerkleTree
from merkle_tree.merkle_tree import _MerkleNode, _NO_ROOT
import unittest

EMPTY_LIST = []
SINGLE_ITEM_LIST = ["ahmed"]
ODD_LENGTH_LIST = ["ahmed", "amine", "yousa"]
EVEN_LENGTH_LIST = ["ahmed", "amine", "yousa", "sara"]


class TestMerkleTree(ABC):

    tree = None
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

    def test_valid_element_in_tree(self):
        for element in self.elements:
            with self.subTest(element=element):
                self.assertTrue(element in self.tree)

    def test_invalid_element_not_in_tree(self):
        self.assertFalse(self.elements[0] + "_" in self.tree)

    def test_proof_is_valid(self):
        for element in self.elements:
            with self.subTest(element=element):
                proof, positions = self.tree.proof(element, return_positions=True)
                self.assertEqual(
                    self.get_root_hash(element, proof, positions), self.root.hash
                )

    @staticmethod
    def get_root_hash(initial, proof, positions):
        return reduce(
            TestMerkleTree._concat_hashes,
            zip(proof, positions), 
            sha256(initial.encode("utf-8")).digest()).hex()

    @staticmethod
    def _concat_hashes(left, right):
        right, position = right
        if position:
            left, right = right, left
        return sha256(left + right).digest()


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

    def test_empty_tree_root_has_no_left_child(self):
        with self.assertRaisesRegex(
            AttributeError, "Empty tree: root has no children"):
            self.tree.root.left
    
    def test_empty_tree_root_has_no_right_child(self):
        with self.assertRaisesRegex(
            AttributeError, "Empty tree: root has no children"):
            self.tree.root.right
    
    def test_empty_tree_root_equals_empty_tree_root(self):
        self.assertTrue(self.tree.root == _NO_ROOT())
    
    def test_empty_tree_root_does_not_equal_non_empty_tree_nodes(self):
        left, right = _MerkleNode("hello"), _MerkleNode("world")
        parent = _MerkleNode(left=left, right=right)
        for node in (left, right, parent):
            with self.subTest(node=node):
                self.assertFalse(self.tree.root == node)
            
    def test_element_in_empty_tree(self):
        self.assertFalse("whatever" in self.tree)

    def test_empty_tree_proof(self):
        self.assertEqual(self.tree.proof("whatever"), [])


class TestMerkleTreeSingle(TestMerkleTree, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.elements = SINGLE_ITEM_LIST
        cls.tree = MerkleTree(SINGLE_ITEM_LIST)
        cls.root = _MerkleNode(SINGLE_ITEM_LIST[0])
        cls.nodes = [[cls.root]]


class TestMerkleTreeOdd(TestMerkleTree, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.elements = ODD_LENGTH_LIST
        cls.tree = MerkleTree(ODD_LENGTH_LIST)
        A, B, C = [_MerkleNode(item) for item in ODD_LENGTH_LIST]
        AB, CC = _MerkleNode(left=A, right=B), _MerkleNode(left=C)
        ABCC = _MerkleNode(left=AB, right=CC) 
        cls.root = ABCC
        cls.nodes = [[ABCC], [AB, CC], [A, B, C, C]]


class TestMerkleTreeEven(TestMerkleTree, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.elements = EVEN_LENGTH_LIST
        cls.tree = MerkleTree(EVEN_LENGTH_LIST)
        A, B, C, D = [_MerkleNode(item) for item in EVEN_LENGTH_LIST]
        AB, CD = _MerkleNode(left=A, right=B), _MerkleNode(left=C, right=D)
        ABCD = _MerkleNode(left=AB, right=CD) 
        cls.root = ABCD
        cls.nodes = [[ABCD], [AB, CD], [A, B, C, D]]

