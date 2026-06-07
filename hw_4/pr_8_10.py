if __name__=='__main__':
    n = int(input())
    a = list()
    for i in range(n):
        sn=input()
        nm=input()
        cl=input()
        dt=input()
        a.append([int(cl[:-1]),cl[-1],sn,nm,dt])
    for i in range(n):
        for j in range(1,n):
            if a[j-1][0]>a[j][0]:
                a[j - 1], a[j] = a[j], a[j - 1]
            elif a[j-1][0]==a[j][0]:
                if a[j-1][1]>a[j][1]:
                    a[j - 1], a[j] = a[j], a[j - 1]
                elif a[j-1][1]==a[j][1]:
                    if a[j-1][2]>a[j][2]:
                        a[j - 1], a[j] = a[j], a[j - 1]
                    elif a[j-1][2]==a[j][2]:
                        if a[j-1][3]>a[j][3]:
                            a[j - 1], a[j] = a[j], a[j - 1]
                        elif a[j-1][3]==a[j][3]:
                            if a[j-1][4]>a[j][4]:
                                a[j - 1], a[j] = a[j], a[j - 1]
    for i in a:
        print(str(i[0])+i[1], *i[2:])