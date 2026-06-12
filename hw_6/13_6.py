if __name__ == '__main__':
    s=input()
    s=s[::-1]
    st=[]
    for i in s:
        if i not in ['+','-','*','/']:
            st.append([i,5])
        else:
            q=st.pop()
            w=st.pop()
            if i=='-':
                if w[1] in ['+','-']:
                    w[0]='('+w[0]+')'
            elif i=='*':
                if q[1] in ['+','-']:
                    q[0]='('+q[0]+')'
                if w[1] in ['+','-']:
                    w[0]='('+w[0]+')'
            elif i=='/':
                if q[1] in ['+','-']:
                    q[0]='('+q[0]+')'
                if w[1]!=5:
                    w[0]='('+w[0]+')'
            res=q[0]+i+w[0]
            st.append([res,i])
    print(st[0][0])
