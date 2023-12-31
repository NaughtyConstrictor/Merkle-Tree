# Merkle-Tree

## Overview
This is a python implementation for a Merkle Tree which is data structure used in blockchain for efficient verification and validation of data.

## Prerequisites
- Python 3.10.9

## Demo
```py
from merkle_tree import MerkleTree

tree = MerkleTree(["ahmed", "amine"])
print(tree.root)
print(tree.root.value)
print(tree.root.hash)
print(tree.nodes)

# output:
# ['ahmed', 'amine']: c794b5771d155548940618b3c71057aee20154b1cf8f8415089aeba15ff6a593
# ['ahmed', 'amine']
# c794b5771d155548940618b3c71057aee20154b1cf8f8415089aeba15ff6a593
# [[['ahmed', 'amine']: c794b5771d155548940618b3c71057aee20154b1cf8f8415089aeba15ff6a593], 
# [['ahmed']: 9af2921d3fd57fe886c9022d1fcc055d53a79e4032fa6137e397583884e1a5de, 
# ['amine']: 54c330d5fa02d666849bbf31f5b97395fe155b38a5ca09c719d279086c214e5e]]
```

## Running tests
You can run tests using Python's built-in `unittest` module. The `-v` flag is optional and can be used for verbose output. For more informations on flags check: <a href="https://docs.python.org/3/library/unittest.html">unittest — Unit testing framework</a>.
```shell
python -m unittest [-v] merkle_tree.test
```

## License
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.
