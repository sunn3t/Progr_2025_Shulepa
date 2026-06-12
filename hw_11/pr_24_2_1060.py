from collections import deque
from copy import copy

if __name__ == '__main__':
    n = int(input())
    data = ['O' * (n + 2)]
    st, fn = None, None
    for i in range(n):
        data.append('O' + input() + 'O')
    data.append('O' * (n + 2))
    # print(data)
    graph = []
    for i in range(n):
        for j in range(n):
            graph.append([])
            if data[i + 1][j + 1] == 'X':
                st = i * n + j
            if data[i + 1][j + 1] == '@':
                fn = i * n + j
            if data[i + 1][j + 1] == 'O':
                continue

            if data[i + 1][j + 2] in '.X@':
                graph[i * n + j].append(i * n + j + 1)
            if data[i][j + 1] in '.X@':
                graph[i * n + j].append((i - 1) * n + j)
            if data[i + 1][j] in '.X@':
                graph[i * n + j].append(i * n + j - 1)
            if data[i + 2][j + 1] in '.X@':
                graph[i * n + j].append((i + 1) * n + j)
    # print(graph)
    dist = {}
    dist[st] = []
    q = deque()
    q.append(st)
    f = 0
    while q:
        v = q.popleft()
        # print(v,dist[v])
        for i in graph[v]:
            if not i in dist:
                dist[i] = copy(dist[v])
                dist[i].append(v)
                q.append(i)
            if i == fn:
                f = 1
                break
        if f == 1:
            break
    # print(dist)
    if not fn in dist:
        print('N')
        exit(0)
    print('Y')
    for i in range(n):
        for j in range(n):
            if i * n + j in dist[fn]:
                print('+', end='')
            else:
                print(data[i + 1][j + 1], end='')
        print()


