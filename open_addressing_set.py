class OpenAddressingSet:
    """
    使用开放地址法（Open Addressing）实现的哈希集合（Set）。
    采用线性探测（Linear Probing）来解决哈希冲突。
    """

    EMPTY = object()  # 特殊标记，区分真正的 `None` 值和空槽

    def __init__(self, initial_capacity=8, growth_factor=2):
        """
        初始化哈希集合。

        :param initial_capacity: 初始哈希表大小（必须是 2 的幂）
        :param growth_factor: 增长因子，当负载因子过高时表扩容
        """
        self.capacity = initial_capacity  # 哈希表容量
        self.size = 0  # 当前元素个数
        self.growth_factor = growth_factor  # 负载过高时的扩展比例
        self.buckets = [self.EMPTY] * self.capacity  # 初始化为空标记

    def _hash(self, key):
        """计算哈希值并映射到表的索引"""
        return hash(key) % self.capacity

    def _probe(self, key):
        """
        线性探测：在哈希表中查找 key 的索引，或者找到第一个空位用于插入。
        """
        index = self._hash(key)
        while self.buckets[index] is not self.EMPTY and self.buckets[index] != key:
            index = (index + 1) % self.capacity  # 线性探测（向后找空位）
        return index

    def add(self, key):
        """
        向集合中添加元素。

        :param key: 要添加的元素
        """
        if self.size / self.capacity >= 0.7:  # 负载因子超过 0.7 就扩容
            self._resize()

        index = self._probe(key)  # 线性探测找到插入位置
        if self.buckets[index] is self.EMPTY:  # 确保插入 `None`
            self.buckets[index] = key
            self.size += 1

    def filter(self, predicate):
        """
        过滤集合中的元素，保留满足 predicate 的元素。

        :param predicate: 过滤函数
        :return: 过滤后的新集合
        """
        new_set = OpenAddressingSet(self.capacity, self.growth_factor)
        for key in self.buckets:
            if key is not self.EMPTY and predicate(key):  # 只保留符合条件的元素
                new_set.add(key)
        return new_set

    def map(self, func):
        """
        映射集合中的元素，返回新集合。

        :param func: 映射函数
        :return: 映射后的新集合
        """
        new_set = OpenAddressingSet(self.capacity, self.growth_factor)
        for key in self.buckets:
            if key is not self.EMPTY:
                new_set.add(func(key))  # 对每个元素应用 `func`
        return new_set

    def reduce(self, func, initial_state):
        """
        归约集合中的元素，返回单一值。

        :param func: 归约函数
        :param initial_state: 初始状态
        :return: 归约结果
        """
        state = initial_state
        for key in self.buckets:
            if key is not self.EMPTY:
                state = func(state, key)  # 累积计算
        return state

    def remove(self, key):
        """
        从集合中删除元素。

        :param key: 要删除的元素
        """
        index = self._hash(key)
        while self.buckets[index] is not self.EMPTY:
            if self.buckets[index] == key:
                self.buckets[index] = self.EMPTY  # 这里用 EMPTY 标记被删除的槽
                self.size -= 1
                return
            index = (index + 1) % self.capacity  # 线性探测继续查找

    def member(self, key):
        """
        判断 key 是否在集合中。

        :param key: 要检查的元素
        :return: 是否存在
        """
        index = self._hash(key)
        while self.buckets[index] is not self.EMPTY:
            if self.buckets[index] == key:  # 确保可以查找 None
                return True
            index = (index + 1) % self.capacity  # 线性探测
        return False

    def _resize(self):
        """
        扩容哈希表，按照增长因子调整大小。
        """
        old_buckets = self.buckets
        self.capacity *= self.growth_factor  # 按照增长因子扩容
        self.buckets = [self.EMPTY] * self.capacity
        self.size = 0

        for key in old_buckets:
            if key is not self.EMPTY:
                self.add(key)  # 重新插入旧元素

    def to_list(self):
        """返回集合元素的列表"""
        return [key for key in self.buckets if key is not self.EMPTY]

    def from_list(self, lst):
        """从列表创建集合"""
        for key in lst:
            self.add(key)

    def __iter__(self):
        """实现迭代器接口"""
        self.iter_index = 0
        return self

    def __next__(self):
        """支持 `next()` 方法"""
        while self.iter_index < self.capacity:
            key = self.buckets[self.iter_index]
            self.iter_index += 1
            if key is not self.EMPTY:
                return key
        raise StopIteration

    @staticmethod
    def empty():
        """返回一个空的集合"""
        return OpenAddressingSet()

    def concat(self, other_set):
        """
        连接两个集合，返回新集合。

        :param other_set: 另一个集合
        """
        new_set = OpenAddressingSet()
        for key in self.buckets:
            if key is not self.EMPTY:
                new_set.add(key)
        for key in other_set.buckets:
            if key is not self.EMPTY:
                new_set.add(key)
        return new_set

