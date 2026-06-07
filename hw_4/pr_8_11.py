if __name__=='__main__':
    n = int(input())
    a = list()
    for i in range(n):
        a.append(int(input()))
    for i in range(n):
        for j in range(1,n):
            if a[j-1]%10>a[j]%10:
                a[j-1],a[j]=a[j],a[j-1]
            elif a[j-1]%10==a[j]%10:
                if a[j-1]>a[j]:
                    a[j - 1], a[j] = a[j], a[j - 1]
    print(*a)