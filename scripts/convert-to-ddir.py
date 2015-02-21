#!/usr/bin/env python

import re

FNAME = "dreams.dre.conv"
dreamStartRegex = re.compile(
        "\* \[([0-9][0-9]*)\] (\(L\) |)([0-9][0-9]/[0-9][0-9]/[0-9][0-9]): ")

def isDreamStart(line):
    m = re.match(dreamStartRegex, line)
    return True if m else False # don't return the MatchObject yet

def parseDate(date):
    """A very quick date parsing hack for this particular case, since my dates
    are already well-formed."""
    month, day, year = date.split('/')
    return "20%s-%s-%s" % (year, month, day)


# split the file by the dream start format mark and read each dream into a
# string in a list
did = 0
drlist = [""] # to avoid dealing with start index of 0
with open(FNAME) as f:
    for line in f:
        if isDreamStart(line):
            did += 1
            drlist.append(line)
        else:
            drlist[did] += line
drlist.pop(0)

# parse into the required elements of the dreamdir format
parsedList = [""]
for i in drlist:
    m = re.match(dreamStartRegex, i)
    did, lcd, date = m.group(1,2,3)
    date = parseDate(date)
    newStr = "Id:\t%05i\nDate:\t%s\n" % (int(did), date)
    if lcd:
        newStr += "Lcd:\t1\n\n"
    else:
        newStr += "\n"
    newStr += ': '.join(i.split(': ')[1:]) # cut out the ID section
    newStr = newStr.strip() + '\n' # remove any trailing newlines, but still EOL
    parsedList.append(newStr)

# write out a dreamdir file for each element of the parsedList
for dream in range(1, len(parsedList)):
    dfilename = "%05i.dre" % dream
    with open(dfilename, 'w') as f:
        f.write(parsedList[dream])
