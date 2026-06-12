if __name__ == '__main__':
    n, m = map(int, input().split())
    graph = []
    for i in range(n):
        l = [0] * n
        graph.append(l)
    for i in range(m):
        a, b = map(int, input().split())
        graph[a - 1][b - 1] += 1
        graph[b - 1][a - 1] += 1

    for i in range(n):
        print(sum(graph[i]))