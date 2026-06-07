def msort(lst):
    if len(lst)>1:
        mid=len(lst)//2
        lh, rh=lst[:mid],lst[mid:]
        msort(lh)
        msort(rh)
        i,j,k=0,0,0
        while i<len(lh) and j<len(rh):
            if lh[i][0]<=rh[j][0]:
                lst[k]=lh[i]
                i+=1
            else:
                lst[k]=rh[j]
                j+=1
            k+=1
        while i<len(lh):
            lst[k]=lh[i]
            i+=1
            k+=1
        while j<len(rh):
            lst[k]=rh[j]
            j+=1
            k+=1
if __name__=='__main__':
    n=int(input())
    lst=[]

    for i in range(n):
        a,b=map(int,input().split())
        lst.append((a,b))
    msort(lst)
    for i in lst:
        print(*i)
