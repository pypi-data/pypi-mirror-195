import random as random_, string


def number(n):
    chars = string.digits 
    s = [random_.choice(chars) for i in range(n)] 
    return ''.join(s)


def string(n):
    chars = string.ascii_letters + string.digits 
    s = [random_.choice(chars) for i in range(n)] 
    return ''.join(s)


