EMPTY = "EMPTY"
DELETED = "DELETED"
N = 100000


def is_prime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


class HashTable:
    def __init__(self, size=100000):
        self._keys = [EMPTY] * size
        self._values = [EMPTY] * size
        self._size = size
        self._count = 0

    def hash(self, s: int):
        return s % self._size

    def rehash(self):
        self._size = self._size * 2 + 1
        while not is_prime(self._size):
            self._size += 2

        _keys = self._keys
        _values = self._values

        self.__init__(self._size)
        for i in range(len(_keys)):
            if _keys[i] != EMPTY:
                self.set(_keys[i], _values[i])

    def set(self, key, value):
        if self._count > 0.7 * self._size:
            self.rehash()

        i = self.hash(key)

        while self._keys[i] != EMPTY:
            if self._keys[i] == key:
                return False
            i = (i + 1) % self._size

        self._keys[i] = key
        self._values[i] = value
        self._count += 1
        return True

    def get(self, key: int):
        i = self.hash(key)
        while self._keys[i] != EMPTY:
            if self._keys[i] == key:
                return self._values[i]
            i = (i + 1) % self._size
        return None


if __name__ == '__main__':
    hash_table = HashTable()
    n = int(input())
    s = list(map(int, input().split()))
    for num in s:
        hash_table.set(num, num)
    print(hash_table._count)