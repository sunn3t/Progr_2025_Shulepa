from math import log


def reconv(x):
    n = len(x)
    for i in range(n - 1):
        x[i + 1] += (x[i] // 10)
        x[i] %= 10
    while x[-1] == 0:
        x.pop()
    return ''.join(list(map(str, x)))[::-1]


def conv(x, y):
    xx = len(x)
    yy = len(y)
    N = max(xx, yy)
    res_x = [0] * (2 ** (int(log(N, 2)) + 1))
    res_y = [0] * (2 ** (int(log(N, 2)) + 1))
    for i in range(xx):
        res_x[i] = int(x[xx - i - 1])
    for i in range(yy):
        res_y[i] = int(y[yy - 1 - i])
    return res_x, res_y


def add(a, b):
    for i in range(min(len(b), len(a))):
        a[i] += b[i]
    return a


def sub(a, b):
    for i in range(len(a)):
        a[i] -= b[i]
    return a


def karacuba(a, b):
    if (len(a) == 1):
        res = [a[0] * b[0]]
        return res
    k = len(a) // 2
    a_1, a_2 = a[:k], a[k:]
    b_1, b_2 = b[:k], b[k:]
    p_1 = karacuba(a_1, b_1)
    p_2 = karacuba(a_2, b_2)
    t_1 = add(a_1, a_2)
    t_2 = add(b_1, b_2)
    t = karacuba(t_1, t_2)
    # print(p_1,t,p_2)
    res1 = [0] * (k) + sub(sub(t, p_1), p_2)
    res2 = add(p_1 + [0] * (2 * k), [0] * (2 * k) + p_2)
    res = add(res2, res1)
    # print(res1)
    # print(res2)
    # print(res)
    # print()
    return res


if __name__ == '__main__':
    a, b = map(str, input().split())
    a, b = conv(a, b)
    # print(a)
    # print(b)
    res = karacuba(a, b)
    # print(res)
    res = reconv(res)
    print(res)


