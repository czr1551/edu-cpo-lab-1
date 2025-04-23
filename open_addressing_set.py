# open_addressing_set.py
from typing import TypeVar, Generic, Callable, Iterator, List, cast

T = TypeVar('T')
U = TypeVar('U')
R = TypeVar('R')


class OpenAddressingSet(Generic[T]):
    """
    A hash set implementation using open addressing with
    linear probing for collision resolution.
    """

    _EMPTY = object()

    def __init__(self, initial_capacity: int = 8,
                 growth_factor: int = 2) -> None:
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.growth_factor: int = growth_factor
        # Buckets store either T or the _EMPTY marker
        self.buckets: List[object] = [self._EMPTY] * self.capacity

    def _hash(self, key: T) -> int:
        return hash(key) % self.capacity

    def _probe(self, key: T) -> int:
        index = self._hash(key)
        while (self.buckets[index] is not self._EMPTY
               and self.buckets[index] != key):
            index = (index + 1) % self.capacity
        return index

    def add(self, key: T) -> None:
        if (self.size + 1) / self.capacity > 0.7:
            self._resize()
        index = self._probe(key)
        if self.buckets[index] is self._EMPTY:
            self.buckets[index] = key
            self.size += 1

    def filter(self, predicate: Callable[[T], bool]) -> 'OpenAddressingSet[T]':
        new_set: OpenAddressingSet[T] = OpenAddressingSet(
            self.capacity, self.growth_factor)
        for item in self:
            if predicate(item):
                new_set.add(item)
        return new_set

    def map(self, func: Callable[[T], U]) -> 'OpenAddressingSet[U]':
        new_set: OpenAddressingSet[U] = OpenAddressingSet(
            self.capacity, self.growth_factor)
        for item in self:
            new_set.add(func(item))
        return new_set

    def reduce(self, func: Callable[[R, T], R], initial_state: R) -> R:
        state: R = initial_state
        for item in self:
            state = func(state, item)
        return state

    def remove(self, key: T) -> None:
        index = self._hash(key)
        while self.buckets[index] is not self._EMPTY:
            if self.buckets[index] == key:
                self.buckets[index] = self._EMPTY
                self.size -= 1
                return
            index = (index + 1) % self.capacity

    def member(self, key: T) -> bool:
        index = self._hash(key)
        while self.buckets[index] is not self._EMPTY:
            if self.buckets[index] == key:
                return True
            index = (index + 1) % self.capacity
        return False

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= self.growth_factor
        self.buckets = [self._EMPTY] * self.capacity
        self.size = 0
        for item in old_buckets:
            if item is not self._EMPTY:
                # type: ignore[arg-type]
                self.add(item)

    def to_list(self) -> List[T]:
        # Cast from List[object] to List[T] since we only store T in non-_EMPTY
        # slots
        return cast(
            List[T], [
                item for item in self.buckets if item is not self._EMPTY])

    def from_list(self, lst: List[T]) -> None:
        for item in lst:
            self.add(item)

    def __iter__(self) -> Iterator[T]:
        self._iter_index: int = 0
        return self

    def __next__(self) -> T:
        while self._iter_index < self.capacity:
            item = self.buckets[self._iter_index]
            self._iter_index += 1
            if item is not self._EMPTY:
                return item  # type: ignore[return-value]
        raise StopIteration

    @staticmethod
    def empty() -> 'OpenAddressingSet[T]':
        return OpenAddressingSet()

    def concat(self, other: 'OpenAddressingSet[T]') -> 'OpenAddressingSet[T]':
        for item in other:
            self.add(item)
        return self

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OpenAddressingSet):
            return False
        if self.size != other.size:
            return False
        for item in self:
            if not other.member(item):
                return False
        return True

    def __len__(self) -> int:
        return self.size
