#!/usr/bin/env python

import os

INPUT_DIRECTORY = '..'
OUTPUT_FILE = 'dotplot-data.csv'

rawL = os.listdir(INPUT_DIRECTORY)
l = [i for i in rawL if i.endswith('.dre')]

outputs = {}
for dreamfile in l:
    with open(INPUT_DIRECTORY + "/" + dreamfile) as f:
        while True:
            line = f.readline().strip()
            if line.startswith('Date:'):
                dateline = line
                break
            # this will crash if there's no date; that's fine for my purposes.

        date = dateline.split('\t')[1]
        year, month, day = date.split('-')
        if (year,month,day) in outputs:
            outputs[(year,month,day)] += 1
        else:
            outputs[(year,month,day)] = 1

order = sorted(outputs.keys())
outstr = ""
for day in order:
    outstr += "%s,%s,%s,%s\n" % (day[0], day[1], day[2], outputs[day])
with open(OUTPUT_FILE, 'w') as f:
    f.write("year, month, day, numdreams\n")
    f.write(outstr)
