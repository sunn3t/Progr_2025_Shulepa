if __name__=='__main__':
    s=input()
    st=[0]
    for i in s:
        if i==')' and st[-1]=='(':
            st.pop()
        elif i==']' and st[-1]=='[':
            st.pop()
        elif i=='}' and st[-1]=='{':
            st.pop()
        else:
            st.append(i)
    if len(st)==1:
        print('yes')
    else:
        print('no')