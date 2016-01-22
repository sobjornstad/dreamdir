#!/usr/bin/env python

"""
Produce data for dreamdir graphs. This script should not be run by itself but
rather by RegeneratePlots.sh.
"""

import ddirparse

OUTPUT_FILE = 'dotplot-data.csv'

dreams = ddirparse.getAttribForAllDreams('Date')
lucids = ddirparse.getAttribForAllDreams('Lucid')
outputs = {}
lucidDays = {}
for dreamNum, attrline in dreams.iteritems():
    date = attrline.split('\t')[1]
    year, month, day = date.split('-')
    if (year,month,day) in outputs:
        outputs[(year,month,day)] += 1
    else:
        outputs[(year,month,day)] = 1
    if dreamNum in lucids:
        lucidDays[(year,month,day)] = 1

order = sorted(outputs.keys())
outstr = ""
for day in order:
    outstr += "%s,%s,%s,%s,%s\n" % (day[0], day[1], day[2], outputs[day],
                                    lucidDays.get(day, 0))
with open(OUTPUT_FILE, 'w') as f:
    f.write("year,month,day,numdreams,lucid\n")
    f.write(outstr)
