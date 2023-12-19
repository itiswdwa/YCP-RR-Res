import random
b = 10000
with open("b.txt",'a+') as f:
    while (b > 0):
        f.write(str(random.randint(100000000,999999999)))
        b -= 1
    