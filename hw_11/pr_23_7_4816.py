import sys

sys.setrecursionlimit(100001)


def dfs(v, graph, use, st):
    use[v] = 1
    st.append(v + 1)
    for i in graph[v]:
        if use[i] == 0:
            dfs(i, graph, use, st)


if __name__ == '__main__':
    n, m = map(int, input().split())
    graph = []
    for i in range(n):
        graph.append([])
    for i in range(m):
        a, b = map(int, input().split())
        graph[a - 1].append(b - 1)
        graph[b - 1].append(a - 1)
    use = [0] * n
    l = []
    for i in range(n):
        if use[i] == 0:
            st = []
            dfs(i, graph, use, st)
            l.append(sorted(st))
    print(len(l))
    for i in l:
        print(len(i))
        print(*i)



