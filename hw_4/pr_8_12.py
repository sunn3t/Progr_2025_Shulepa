global array
def qsort(array, a, b):
    if a>=b:
        return
    piv=array[a+(b-a)//2]
    l,r=a,b
    while True:
        while array[l]<piv:
            l+=1
        while array[r]>piv:
            r-=1
        if l>=r:
            break
        array[l],array[r]=array[r],array[l]
        l+=1
        r-=1
    qsort(array,a,r)
    qsort(array,r+1,b)

if __name__=='__main__':
    n=int(input())
    array=list(map(int,input().split()))
    qsort(array,0,len(array)-1)
    print(*array)