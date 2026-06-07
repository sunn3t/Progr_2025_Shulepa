def A(n, k, l):
    if k == 0:
        print(*l)
        return
    for i in range(1, n + 1):
        if i not in l:
            l.append(i)
            A(n, k - 1, l)
            l.pop()


if __name__ == '__main__':
    n, k = map(int, input().split())
    A(n, k, [])
