def fun(s, l, m):
    M = s
    for i in range(len(l)):
        if s + l[i] > m:
            continue
        el = fun(s + l[i], l[i + 1:], m)
        M = max(M, el)
        if M == m:
            return M
    return M


if __name__ == '__main__':
    f = open('input.txt')
    for line in f.readlines():
        l = list(map(int, line.split()))
        n, l = l[0], l[2:]
        print('sum:', fun(0, l, n), sep='')

    f.close()