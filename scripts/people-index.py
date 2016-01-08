#!/usr/bin/env python

"""
Produce an index of all the people in the dreamdir and the dreams they occur
in. There is a friendly-looking output and one suitable for producing a LaTeX
index, selectable with the '--index' command-line parameter for LaTeX mode.

See also places-index.py.
"""

import ddirparse
import sys

# manual inversion/sorting
nameExceptions = {
    'Margaret de Veer': 'de Veer, Margaret',
}

def mungeNames(item):
    # is this an exception?
    if item in nameExceptions:
        return nameExceptions[item]

    # if there are two elements, separated by a space, take those as first
    # and last name and invert them
    sitem = item.split(' ')
    if len(sitem) == 2:
        item = sitem[1] + ", " + sitem[0]

    return item


### MAIN ###
if len(sys.argv) > 1 and sys.argv[1] == "--index":
    indexMode = True
    OUTPUT_FILE = '/home/soren/current/drbook/resources/people-index.tex'
else:
    indexMode = False
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

# invert first/last names where appropriate
newPeopleDict = {}
for item in peopleDict:
    newPeopleDict[mungeNames(item)] = peopleDict[item]
peopleDict = newPeopleDict

# make CSV
order = sorted(peopleDict.keys(), key=str.lower)
outstr = ""
for person in order:
    dreamList = ', '.join([str(i) for i in sorted(peopleDict[person])])
    if indexMode:
        outstr += "\\item {%s}, %s\n" % (person, dreamList)
    else:
        outstr += "%s,%s,%s\n" % (person, len(peopleDict[person]), dreamList)
with open(OUTPUT_FILE, 'w') as f:
    if not indexMode:
        f.write("person, numdreams, dreamlist\n")
    f.write(outstr)
