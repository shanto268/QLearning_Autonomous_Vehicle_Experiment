import random
import numpy as np

"""
lanes = [] #initialize lane array
for x in range(3): #loops for number of lanes to be created 
    lanes.append( [None] * 100 ) #creates empty lane of None values with desired length                                           

av = 1
hv = 99
tot = [1 for i in range(hv)]
tot += [2 for j in range(1)]
random.shuffle(tot)

while len(tot) != 0:
    x = random.randint(0,99)
    y = random.randint(0,2)
    if lanes[y][x] == None:
        val = tot.pop()
        if val == 1:
            typ = "HV"
        else:
            typ = "AV"
        print("(x,y,type) ", x,y,typ)
    else:
        x = random.randint(0,99)
        y = random.randint(0,2)
"""
n = 100
num1 = [random.randint(0,100) for i in range(n)] 
print(num1)
ii = np.split(np.array(num1),n/10)
