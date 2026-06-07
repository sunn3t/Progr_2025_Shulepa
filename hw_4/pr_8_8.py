if __name__ == '__main__':
    n = int(input())
    a = list()
    for i in range(n):
        x,y,z=map(int,input().split())
        a.append(x*10000+y*100+z)
    for i in range(n):
        for j in range(1, n):
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
    for i in range(n):
        print(a[i]//10000,(a[i]//100)%100,a[i]%100)