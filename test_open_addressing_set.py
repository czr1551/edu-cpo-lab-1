from typing import List
from hypothesis import given, strategies as st
from open_addressing_set import OpenAddressingSet


def create_set(lst: List[int]) -> OpenAddressingSet[int]:
    s: OpenAddressingSet[int] = OpenAddressingSet()
    s.from_list(lst)
    return s

# -----------------------
# Basic Functionality Tests
# -----------------------


def test_add() -> None:
    s: OpenAddressingSet[int] = OpenAddressingSet()
    s.add(10)
    s.add(20)
    assert s.member(10) is True
    assert s.member(20) is True
    assert s.member(30) is False  # Non-existent element


def test_remove() -> None:
    s: OpenAddressingSet[int] = OpenAddressingSet()
    s.add(10)
    s.add(20)
    s.remove(10)
    assert s.member(10) is False
    assert s.member(20) is True


def test_size() -> None:
    s: OpenAddressingSet[int] = OpenAddressingSet()
    assert s.size == 0
    s.add(10)
    s.add(20)
    assert s.size == 2
    s.remove(10)
    assert s.size == 1


def test_to_list() -> None:
    s: OpenAddressingSet[int] = OpenAddressingSet()
    s.add(10)
    s.add(20)
    assert sorted(s.to_list()) == [10, 20]


def test_from_list() -> None:
    s: OpenAddressingSet[int] = OpenAddressingSet()
    s.from_list([1, 2, 3])
    assert s.member(1) is True
    assert s.member(2) is True
    assert s.member(3) is True
    assert s.member(4) is False

# -----------------------
# Iterator Tests
# -----------------------


def test_iterator() -> None:
    s: OpenAddressingSet[int] = OpenAddressingSet()
    s.from_list([1, 2, 3])
    result: List[int] = list(iter(s))
    assert sorted(result) == [1, 2, 3]

# -----------------------
# Filter, Map, and Reduce
# -----------------------


def test_filter() -> None:
    s: OpenAddressingSet[int] = OpenAddressingSet()
    s.from_list([1, 2, 3, 4, 5])
    even_set: OpenAddressingSet[int] = s.filter(lambda x: x % 2 == 0)
    assert sorted(even_set.to_list()) == [2, 4]


def test_map() -> None:
    s: OpenAddressingSet[int] = OpenAddressingSet()
    s.from_list([1, 2, 3])
    squared_set: OpenAddressingSet[int] = s.map(lambda x: x ** 2)
    assert sorted(squared_set.to_list()) == [1, 4, 9]


def test_reduce() -> None:
    s: OpenAddressingSet[int] = OpenAddressingSet()
    s.from_list([1, 2, 3, 4])
    total: int = s.reduce(lambda acc, x: acc + x, 0)
    assert total == 10  # 1+2+3+4 = 10

# -----------------------
# Monoid (empty & concat) Tests
# -----------------------


def test_empty() -> None:
    s: OpenAddressingSet[int] = OpenAddressingSet.empty()
    assert s.size == 0


def test_concat() -> None:
    s1: OpenAddressingSet[int] = OpenAddressingSet()
    s1.from_list([1, 2, 3])
    s2: OpenAddressingSet[int] = OpenAddressingSet()
    s2.from_list([4, 5])
    s1.concat(s2)
    assert sorted(s1.to_list()) == [1, 2, 3, 4, 5]

# -----------------------
# Property-Based Tests for Monoid Properties
# -----------------------


@given(st.lists(st.integers()))
def test_identity_property(lst: List[int]) -> None:
    # a.concat(empty()) == a
    a: OpenAddressingSet[int] = create_set(lst)
    a_copy: OpenAddressingSet[int] = create_set(lst)
    a.concat(OpenAddressingSet.empty())
    assert sorted(a.to_list()) == sorted(a_copy.to_list())

    # empty().concat(a) == a
    a2: OpenAddressingSet[int] = create_set(lst)
    empty_set: OpenAddressingSet[int] = OpenAddressingSet.empty()
    empty_set.concat(a2)
    assert sorted(empty_set.to_list()) == sorted(a2.to_list())


@given(
    st.lists(st.integers()),
    st.lists(st.integers()),
    st.lists(st.integers())
)
def test_associativity_property(
    lst_a: List[int],
    lst_b: List[int],
    lst_c: List[int]
) -> None:
    # (a.concat(b)).concat(c)
    a1: OpenAddressingSet[int] = create_set(lst_a)
    b1: OpenAddressingSet[int] = create_set(lst_b)
    c1: OpenAddressingSet[int] = create_set(lst_c)
    a1.concat(b1).concat(c1)
    left: List[int] = sorted(a1.to_list())

    # a.concat(b.concat(c))
    a2: OpenAddressingSet[int] = create_set(lst_a)
    b2: OpenAddressingSet[int] = create_set(lst_b)
    c2: OpenAddressingSet[int] = create_set(lst_c)
    b2.concat(c2)
    a2.concat(b2)
    right: List[int] = sorted(a2.to_list())

    assert left == right

# -----------------------
# Handling `None` Values
# -----------------------


def test_none_value() -> None:
    s: OpenAddressingSet[None] = OpenAddressingSet()
    s.add(None)
    assert s.member(None) is True
    s.remove(None)
    assert s.member(None) is False

# -----------------------
# Testing Hash Set Resizing Logic
# -----------------------


def test_resize() -> None:
    # Test 1: Capacity change when resizing is triggered
    s: OpenAddressingSet[int] = OpenAddressingSet(
        initial_capacity=4, growth_factor=2)
    assert s.capacity == 4
    s.add(1)
    s.add(2)
    s.add(3)
    assert s.capacity == 8
    assert sorted(s.to_list()) == [1, 2, 3]

    # Test 2: Correctness of elements after resizing
    s.add(4)
    s.add(5)
    assert s.capacity == 8
    s.add(6)
    assert s.capacity == 16
    expected: List[int] = [1, 2, 3, 4, 5, 6]
    assert sorted(s.to_list()) == expected

    # Test 3: Resizing after deleting elements
    s.remove(3)
    s.remove(5)
    for v in [7, 8, 9, 10, 11, 12, 13, 14]:
        s.add(v)
    assert s.capacity == 32
    expected_after_remove: List[int] = [
        1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    assert sorted(s.to_list()) == expected_after_remove

    # Test 4: Special case with initial capacity of 1
    s_small: OpenAddressingSet[int] = OpenAddressingSet(
        initial_capacity=1, growth_factor=2)
    s_small.add(0)
    assert s_small.capacity == 2
    s_small.add(1)
    assert s_small.capacity == 4
    assert sorted(s_small.to_list()) == [0, 1]

# -----------------------
# Randomized Testing (Hypothesis)
# -----------------------


@given(st.lists(st.integers()))
def test_from_list_to_list_equality(lst: List[int]) -> None:
    s: OpenAddressingSet[int] = OpenAddressingSet()
    s.from_list(lst)
    assert sorted(s.to_list()) == sorted(set(lst))


@given(st.lists(st.integers()))
def test_python_len_and_set_size_equality(lst: List[int]) -> None:
    s: OpenAddressingSet[int] = OpenAddressingSet()
    s.from_list(lst)
    assert s.size == len(set(lst))
