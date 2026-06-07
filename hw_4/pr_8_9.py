def w(a):
    res=0
    for i in a:
        res+=int(i)
    return res
if __name__ == '__main__':
    n = int(input())
    k=int(input())
    a=list(map(str,list(range(1,n+1))))
    ind=k-1
    for i in range(n):
        for j in range(1,n):
            if w(a[j-1])>w(a[j]):
                if a[ind]==a[j]:
                    ind-=1
                elif a[ind]==a[j-1]:
                    ind+=1
                a[j-1],a[j]=a[j],a[j-1]

            elif w(a[j-1])==w(a[j]):
                if a[j-1]>a[j]:
                    if a[ind] == a[j]:
                        ind -= 1
                    elif a[ind] == a[j - 1]:
                        ind += 1
                    a[j - 1], a[j] = a[j], a[j - 1]
    print(ind+1)
    print(a[k-1])
