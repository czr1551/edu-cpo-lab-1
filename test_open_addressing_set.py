from hypothesis import given, strategies as st
from open_addressing_set import OpenAddressingSet

# -----------------------
# Basic Functionality Tests
# -----------------------


def test_add():
    s = OpenAddressingSet()
    s.add(10)
    s.add(20)
    assert s.member(10) is True
    assert s.member(20) is True
    assert s.member(30) is False  # Non-existent element


def test_remove():
    s = OpenAddressingSet()
    s.add(10)
    s.add(20)
    s.remove(10)
    assert s.member(10) is False
    assert s.member(20) is True


def test_size():
    s = OpenAddressingSet()
    assert s.size == 0
    s.add(10)
    s.add(20)
    assert s.size == 2
    s.remove(10)
    assert s.size == 1


def test_to_list():
    s = OpenAddressingSet()
    s.add(10)
    s.add(20)
    assert sorted(s.to_list()) == [10, 20]


def test_from_list():
    s = OpenAddressingSet()
    s.from_list([1, 2, 3])
    assert s.member(1) is True
    assert s.member(2) is True
    assert s.member(3) is True
    assert s.member(4) is False

# -----------------------
# Iterator Tests
# -----------------------


def test_iterator():
    s = OpenAddressingSet()
    s.from_list([1, 2, 3])
    result = list(iter(s))
    assert sorted(result) == [1, 2, 3]

# -----------------------
# Filter, Map, and Reduce
# -----------------------


def test_filter():
    s = OpenAddressingSet()
    s.from_list([1, 2, 3, 4, 5])
    even_set = s.filter(lambda x: x % 2 == 0)
    assert sorted(even_set.to_list()) == [2, 4]


def test_map():
    s = OpenAddressingSet()
    s.from_list([1, 2, 3])
    squared_set = s.map(lambda x: x ** 2)
    assert sorted(squared_set.to_list()) == [1, 4, 9]


def test_reduce():
    s = OpenAddressingSet()
    s.from_list([1, 2, 3, 4])
    total = s.reduce(lambda acc, x: acc + x, 0)
    assert total == 10  # 1+2+3+4 = 10

# -----------------------
# Monoid (empty & concat)
# -----------------------


def test_empty():
    s = OpenAddressingSet.empty()
    assert s.size == 0


def test_concat():
    s1 = OpenAddressingSet()
    s1.from_list([1, 2, 3])

    s2 = OpenAddressingSet()
    s2.from_list([4, 5])

    s3 = s1.concat(s2)
    assert sorted(s3.to_list()) == [1, 2, 3, 4, 5]

# -----------------------
# Handling `None` Values
# -----------------------


def test_none_value():
    s = OpenAddressingSet()
    s.add(None)
    assert s.member(None) is True
    s.remove(None)
    assert s.member(None) is False

# -----------------------
# Testing Hash Set Resizing Logic
# -----------------------


def test_resize():
    # Test 1: Capacity change when resizing is triggered
    s = OpenAddressingSet(initial_capacity=4, growth_factor=2)
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
    expected = [1, 2, 3, 4, 5, 6]
    assert sorted(s.to_list()) == expected

    # Test 3: Resizing after deleting elements, ensuring deleted elements are not migrated
    s.remove(3)
    s.remove(5)
    s.add(7)
    s.add(8)
    s.add(9)
    s.add(10)
    s.add(11)
    s.add(12)
    s.add(13)
    s.add(14)
    assert s.capacity == 32
    expected_after_remove = [1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    assert sorted(s.to_list()) == expected_after_remove

    # Test 4: Special case with initial capacity of 1
    s = OpenAddressingSet(initial_capacity=1, growth_factor=2)
    s.add(0)
    assert s.capacity == 2
    s.add(1)
    assert s.capacity == 4
    assert sorted(s.to_list()) == [0, 1]

# -----------------------
# Randomized Testing (Hypothesis)
# -----------------------


@given(st.lists(st.integers()))
def test_from_list_to_list_equality(lst):
    s = OpenAddressingSet()
    s.from_list(lst)
    assert sorted(s.to_list()) == sorted(set(lst))


@given(st.lists(st.integers()))
def test_python_len_and_set_size_equality(lst):
    s = OpenAddressingSet()
    s.from_list(lst)
    assert s.size == len(set(lst))
