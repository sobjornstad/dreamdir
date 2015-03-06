#!/usr/bin/env python

import ddirparse

OUTPUT_FILE = 'people-list.csv'

outputs = {}
dreams = ddirparse.getAttribForAllDreams('People')

# get list of unique people
people = dreams.values()
uniquePeople = []
for p in people:
    ps = p.split('\t')[1].split(',')
    for q in ps:
        if q.strip() not in uniquePeople:
            uniquePeople.append(q.strip())

# make clean dict of dreams, with people as a list
cleanDreams = {}
for d in dreams:
    splitted = dreams[d].split('\t')[1].split(',')
    cleanDreams[d] = [i.strip() for i in splitted]

# populate dictionary with empty lists for each person
peopleDict = {}
for p in uniquePeople:
    if p not in peopleDict:
        peopleDict[p] = []

# fill said lists with dream numbers
for d in dreams:
    for p in uniquePeople:
        if p in cleanDreams[d]:
            peopleDict[p].append(d)

# make CSV
order = sorted(peopleDict.keys())
outstr = ""
for person in order:
    dreamList = ' '.join([str(i) for i in peopleDict[person]])
    outstr += "%s,%s,%s\n" % (person, len(peopleDict[person]), dreamList)
with open(OUTPUT_FILE, 'w') as f:
    f.write("person, numdreams, dreamlist\n")
    f.write(outstr)
