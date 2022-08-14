import math


def exp(x):
    return math.e ** (x**2)

def mugen(x):
    return math.sqrt(x**2 - x**4)

def exp2(x):
    return x ** x

def sinsq(x):
    return math.sin(x)**2

def sin_rec(x):
    if x != 0:
        return math.sin(1/x)
    else:
        return 0

def ntan(x):
    return -math.tan(x)

def mytan(n):
    return lambda x: math.tan(x) + n

def myntan(n):
    return lambda x: -math.tan(x) + n

def create_tans():
    tans = []
    for i in range(-10, 11, 2):
        tans.append(mytan(i))
        tans.append(myntan(i))
    return tans

def cot(x):
    try:
        return 1/math.tan(x)
    except:
        return 0 

def kaidan(x):
    return math.e**math.sin(x) + x
