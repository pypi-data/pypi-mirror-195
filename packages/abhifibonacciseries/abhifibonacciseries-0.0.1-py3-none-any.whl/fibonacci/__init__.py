from math import *

def CheckFibonacci(num):
    
    def IsPerfectSquare(num):
        s=int(sqrt(num))
        return(s*s==num)
    
    def IsFibonacci(num):
        return IsPerfectSquare(5*num*num-4) or IsPerfectSquare(5*num*num+4)
    
    return IsFibonacci(num)

def PrintFibonacci(num):
    list=[0,1]
    a=0
    b=1
    for i in range(num-2):
        c=a+b
        list.append(c)
        a=b
        b=c
    print(list)
