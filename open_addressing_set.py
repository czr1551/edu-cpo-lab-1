from typing import Any, Callable, List, Optional, Iterator


class OpenAddressingSet:
    """
    A hash set implementation using open addressing with
    linear probing for collision resolution.
    """

    EMPTY = object()
    # Special marker to distinguish between `None` and empty slots

    def __init__(self: 'OpenAddressingSet', initial_capacity: int = 8,
                 growth_factor: int = 2) -> None:
        """
        Initialize the hash set.

        :param initial_capacity:
        Initial size of the hash table (must be a power of 2)
        :param growth_factor:
        Growth factor for table expansion when load factor is too high
        """
        self.capacity = initial_capacity
        self.size = 0
        self.growth_factor = growth_factor
        self.buckets = [self.EMPTY] * self.capacity

    def _hash(self: 'OpenAddressingSet', key: int) -> int:
        """Compute the hash value and map it to a table index."""
        return hash(key) % self.capacity

    def _probe(self: 'OpenAddressingSet', key: int) -> int:
        """
        Linear probing: Find the index of the key in the hash table
        or the first empty slot for insertion.
        """
        index = self._hash(key)
        while (self.buckets[index] is not self.EMPTY
               and self.buckets[index] != key):
            index = (index + 1) % self.capacity
        return index

    def add(self: 'OpenAddressingSet', key: int) -> None:
        """
        Add an element to the set.

        :param key: The element to add
        """
        if (self.size + 1) / self.capacity > 0.7:
            self._resize()

        index = self._probe(key)
        if self.buckets[index] is self.EMPTY:
            self.buckets[index] = key
            self.size += 1

    def filter(self: 'OpenAddressingSet',
               predicate: Callable[[int], bool]) -> 'OpenAddressingSet':
        """
        Filter elements in the set, retaining those that satisfy the predicate.

        :param predicate: The filtering function
        :return: A new set with filtered elements
        """
        new_set = OpenAddressingSet(self.capacity, self.growth_factor)
        for key in self.buckets:
            if key is not self.EMPTY and predicate(key):
                new_set.add(key)
        return new_set

    def map(self: 'OpenAddressingSet',
            func: Callable[[int], int]) -> 'OpenAddressingSet':
        """
        Map elements in the set, returning a new set.

        :param func: The mapping function
        :return: A new set with mapped elements
        """
        new_set = OpenAddressingSet(self.capacity, self.growth_factor)
        for key in self.buckets:
            if key is not self.EMPTY:
                new_set.add(func(key))
        return new_set

    def reduce(self: 'OpenAddressingSet', func: Callable[[Any, int], Any],
               initial_state: Any) -> Any:
        """
        Reduce elements in the set to a single value.

        :param func: The reduction function
        :param initial_state: The initial state
        :return: The result of reduction
        """
        state = initial_state
        for key in self.buckets:
            if key is not self.EMPTY:
                state = func(state, key)
        return state

    def remove(self: 'OpenAddressingSet', key: int) -> None:
        """
        Remove an element from the set.

        :param key: The element to remove
        """
        index = self._hash(key)
        while self.buckets[index] is not self.EMPTY:
            if self.buckets[index] == key:
                self.buckets[index] = self.EMPTY
                self.size -= 1
                return
            index = (index + 1) % self.capacity

    def member(self: 'OpenAddressingSet', key: int) -> bool:
        """
        Check if an element exists in the set.

        :param key: The element to check
        :return: Whether the element exists
        """
        index = self._hash(key)
        while self.buckets[index] is not self.EMPTY:
            if self.buckets[index] == key:
                return True
            index = (index + 1) % self.capacity
        return False

    def _resize(self: 'OpenAddressingSet') -> None:
        """
        Expand the hash table according to the growth factor.
        """
        old_buckets = self.buckets
        self.capacity *= self.growth_factor
        self.buckets = [self.EMPTY] * self.capacity
        self.size = 0

        for key in old_buckets:
            if key is not self.EMPTY:
                self.add(key)

    def to_list(self: 'OpenAddressingSet') -> List[int]:
        """Convert the set to a Python list."""
        return [key for key in self.buckets if key is not self.EMPTY]

    def from_list(self: 'OpenAddressingSet', lst: List[int]) -> None:
        """Create a set from a list."""
        for key in lst:
            self.add(key)

    def __iter__(self: 'OpenAddressingSet') -> Iterator[int]:
        """Implement the iterator interface."""
        self.iter_index = 0
        return self

    def __next__(self: 'OpenAddressingSet') -> int:
        """Support the `next()` method."""
        while self.iter_index < self.capacity:
            key = self.buckets[self.iter_index]
            self.iter_index += 1
            if key is not self.EMPTY:
                return key
        raise StopIteration

    @staticmethod
    def empty() -> 'OpenAddressingSet':
        """Return an empty set."""
        return OpenAddressingSet()

    def concat(self: 'OpenAddressingSet',
               other_set: 'OpenAddressingSet') -> 'OpenAddressingSet':
        for key in other_set.buckets:
            if key is not self.EMPTY:
                self.add(key)
        return self
