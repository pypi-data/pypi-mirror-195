def CheckArmstrong(num):
    sum = 0
    lent = 0
    temp=num
    while temp!=0:
        lent=lent+1
        temp=int(temp/10)

    temp = num
    while temp > 0:
        digit = temp % 10
        sum += digit ** lent
        temp //= 10


    if num == sum:
        return(True)
    else:
        return(False)
    
def ListArmstrong(num):
    list1=[]
    i=0
    while(len(list1)<num):
        temp=i
        sum=0
        lent=0
        while temp!=0:
            lent=lent+1
            temp=int(temp/10)

        temp = i
        while temp > 0:
            digit = temp % 10
            sum += digit ** lent
            temp //= 10
        if(sum==i):
            list1.append(i)
        i=i+1
    return(list1)
    