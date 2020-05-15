import operator
import time
start = time.time()
with open('a.txt', mode='w') as f:
    for i in range(1000):
        f.write('\n')
        f.write(str(i))



