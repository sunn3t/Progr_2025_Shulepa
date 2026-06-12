import sys

sys.setrecursionlimit(10001)


def dfs(v, graph, use):
    use[v[0]][v[1]] = 1
    for i in graph[v]:
        if use[i[0]][i[1]] == 0:
            dfs(i, graph, use)


if __name__ == '__main__':
    n, m = map(int, input().split())
    data = ['.' * (m + 2)]
    st, fn = None, None
    for i in range(n):
        data.append('.' + input() + '.')
    data.append('.' * (m + 2))
    # print(data)
    graph = {}
    use = []
    for i in range(n):
        use.append([0] * m)
        for j in range(m):
            graph[(i, j)] = []
            if data[i + 1][j + 1] == '.':
                continue

            if data[i + 1][j + 2] == '#':
                graph[(i, j)].append((i, j + 1))
            if data[i][j + 1] == '#':
                graph[(i, j)].append((i - 1, j))
            if data[i + 1][j] == '#':
                graph[(i, j)].append((i, j - 1))
            if data[i + 2][j + 1] == '#':
                graph[(i, j)].append((i + 1, j))
    cnt = 0
    for i in range(n):
        for j in range(m):
            if use[i][j] == 0 and data[i + 1][j + 1] == '#':
                dfs((i, j), graph, use)
                cnt += 1
    print(cnt)