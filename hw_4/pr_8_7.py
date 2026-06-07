if __name__=='__main__':
    n = int(input())
    a = list(map(int, input().split()))

    for i in range(1,n):
        f=0
        cv=a[i]
        pos=i
        while pos>0:
            if a[pos-1]>cv:
                a[pos]=a[pos-1]
                f=1
            else:
                break
            pos-=1
        a[pos]=cv
        if f==1:
            print(*a)
