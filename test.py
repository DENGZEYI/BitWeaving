import operator
import time
start = time.time()
with open('a.txt', mode='w') as f:
    for i in range(1000):
        f.write('\n')
        f.write(str(i))


list = []
with open('a.txt', mode='r') as f:
    for line in f:
        list.append(line)

print(time.time()-start)
