EMPTY = "EMPTY"


def is_prime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


class HashTable:

    def __init__(self, size=1000):
        self._keys = [EMPTY] * size
        self._values = [EMPTY] * size
        self._size = size
        self._count = 0

    def hash(self, s: str):
        h = 0
        for i in range(len(s)):
            h = h * 29 + ord(s[i])
        return h % self._size

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
                self._values[i] = value
                return False
            i = (i + 1) % self._size

        self._keys[i] = key
        self._values[i] = value
        self._count += 1
        return True

    def get(self, key):
        i = self.hash(key)
        while self._keys[i] != EMPTY:
            if self._keys[i] == key:
                return self._values[i]
            i = (i + 1) % self._size
        return None


if __name__ == '__main__':
    n, m = map(int, input().split())
    hashtable = HashTable()
    for i in range(n):
        word = input().strip().lower()
        hashtable.set(word, False)

    f = 0
    for i in range(m):
        line = input().lower()
        word = ""
        for ch in line:
            if 'A' <= ch <= 'Z':
                ch = chr(ch + 'a' - 'A')
                word += ch
            elif 'a' <= ch <= 'z':
                word += ch
            else:
                if word:
                    s = hashtable.get(word)
                    if s is None:
                        print("Some words from the text are unknown.")
                        exit(0)
                    hashtable.set(word, True)
                    word = ""

        if word:
            s = hashtable.get(word)
            if s is None:
                print("Some words from the text are unknown.")
                exit(0)
            hashtable.set(word, True)

    for key in hashtable._keys:
        if key != EMPTY:
            if hashtable.get(key) is False:
                print("The usage of the vocabulary is not perfect.")
                exit(0)

    print("Everything is going to be OK.")