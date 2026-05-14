#!/usr/bin/python2
import ddirparse
import matplotlib
import matplotlib.pyplot as plt

HEADER = 'People'
VALUE = 'Nichi Smith'

headers = ddirparse.getAllHeaders()

matched = set()
for k, v in sorted(headers.items()):
    if VALUE in (i.strip() for i in v.get(HEADER, '').split(',')):
        matched.add(int(k))

data = []
for dream in range(1, len(headers)+1):
    if 1 <= dream <= 100:
        denom = dream
    else:
        denom = 100
    portion = float(sum(1 for i in range(max(1, dream-100), dream) if i in matched)) / denom
    data.append((dream, portion))

#figure, axes = plt.subplots()
plt.plot(list(i[0] for i in data), list(i[1] for i in data))
plt.show()
