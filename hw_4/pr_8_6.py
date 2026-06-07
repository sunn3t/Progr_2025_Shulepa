if __name__ == '__main__':
    n = int(input())
    a = list()
    for i in range(n):
        x = input()
        a.append(x)

    for j in range(n):
        mi = 0
        for i in range(n - j):
            if a[i] > a[mi]:
                mi = i
        a[n - j - 1], a[mi] = a[mi], a[n - j - 1]
    print(*a, sep='\n')

