# GROUP-NO DAY OFF - lab 1 - variant "Set based on hash map, open addressing"

This project implements a Set based on Hash Map (Open Addressing) and demonstrates mutable data structure implementation. It follows proper project structure and CI checks. While not optimized for production, it serves as an educational example.

## Project structure

- open_addressing_set.py — Implementation of OpenAddressingSet class with add, remove, member, filter, map, reduce, and other features.
- test_open_addressing_set.py — Unit tests and Property-Based Tests (PBT) for OpenAddressingSet.

## Features

- Core functionality:
  - add(key): Add an element.
  - remove(key): Remove an element.
  - member(key): Check if an element exists.
  - size(): Get the number of elements.
  - from_list(lst): Create a set from a Python list.
  - to_list(): Convert the set to a Python list.
  - concat(set): Merge two sets.
- Functional operations:
  - filter(predicate): Return a new set with elements that satisfy the predicate.
  - map(func): Apply a function to all elements and return a new set.
  - reduce(func, initial_state): Aggregate values using a given function.
- PBT:
  - test_from_list_to_list_equality
  - test_python_len_and_set_size_equality
  - test_add_commutative
- Monoid properties:
  - empty(): Create an empty set.
  - concat(set): Combine two sets.

## Contribution

- czr61551@gmail.com (EMAIL) -- Implementation of OpenAddressingSet, documentation.
- quinn_wang0416@163.com (EMAIL) -- Implementation of test cases.

## Changelog

- 12.02.2025 - 2
  - Refactored _probe() to correctly handle empty slots.
- 11.02.2025 - 1
  - Improved test coverage
- 10.02.2025 - 0
  - Initial implementation of OpenAddressingSet.
  - Basic tests for add(), remove(), and member().

## Design notes

- Used open addressing with linear probing for collision resolution.
- Used a special marker EMPTY to distinguish deleted elements from None.
- Ensured logarithmic growth factor to maintain efficient resizing.
- Designed unit tests and PBT to validate properties of OpenAddressingSet.
- Followed PEP8 and CI best practices with pytest, ruff, mypy, and coverage.




