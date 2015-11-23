#!/usr/bin/env python

import ddirparse
import sys

# manual changes
nameExceptions = {
    #'VU': 'Valparaiso University',
    #'VHS': 'Valparaiso High School',
    #'TLC': 'Trinity Lutheran Church',
    #'BFMS': 'Benjamin Franklin Middle School',
    #'CHM': 'Christiansen Hall of Music',
}

def mungeNames(item):
    # is this an exception?
    if item in nameExceptions:
        return nameExceptions[item]
    else:
        return item


### MAIN ###
OUTPUT_FILE = '/home/soren/current/drbook/resources/places-index.tex'

outputs = {}
dreams = ddirparse.getAttribForAllDreams('Places')

# get list of unique people
places = dreams.values()
uniquePlaces = []
for p in places:
    ps = p.split('\t')[1].split(',')
    for q in ps:
        if q.strip() not in uniquePlaces:
            uniquePlaces.append(q.strip())

# make clean dict of dreams, with people as a list
cleanDreams = {}
for d in dreams:
    splitted = dreams[d].split('\t')[1].split(',')
    cleanDreams[d] = [i.strip() for i in splitted]

# populate dictionary with empty lists for each place
placesDict = {}
for p in uniquePlaces:
    if p not in placesDict:
        placesDict[p] = []

# fill said lists with dream numbers
for d in dreams:
    for p in uniquePlaces:
        if p in cleanDreams[d]:
            placesDict[p].append(d)

# change names where appropriate
newPlacesDict = {}
for item in placesDict:
    newPlacesDict[mungeNames(item)] = placesDict[item]
placesDict = newPlacesDict

# make CSV
order = sorted(placesDict.keys(), key=str.lower)
outstr = ""
for place in order:
    dreamList = ', '.join([str(i) for i in placesDict[place]])
    outstr += "\\item {%s}, %s\n" % (place, dreamList)
with open(OUTPUT_FILE, 'w') as f:
    f.write(outstr)
