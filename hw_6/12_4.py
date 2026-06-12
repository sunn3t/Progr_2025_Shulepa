if __name__ == '__main__':
    while True:
        n=int(input())
        if n==0:
            break
        while True:
            lst=list(map(int,input().split()))
            if lst[0]==0:
                print()
                break
            st,k=[0],0
            for i in range(1,n+1):
                st.append(i)
                while k<n and st[-1]==lst[k]:
                    st.pop()
                    k+=1
            #print(st)
            if len(st)==1:
                print('Yes')
            else:
                print('No')