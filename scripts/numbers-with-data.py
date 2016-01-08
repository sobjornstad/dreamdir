#!/usr/bin/env python

"""
Produce a tab-delimited list of all dreams and the HEADER values for each.
A dream number will be omitted if that dream has no given HEADER.

Example output from my dreamdir when HEADER is "People":
    number	people
    1	Albert Einstein
    4	Grandma
    6	Mrs. Nagel, Oksana Creech, Timothy McLean
    7	Oksana Creech
    8	Mama
    [...]
"""

import ddirparse
import sys

### MAIN ###
HEADER = "People"
OUTPUT_FILE = 'nums-with-people.csv'

outputs = {}
dreams = ddirparse.getAttribForAllDreams(HEADER)

with open(OUTPUT_FILE, 'w') as f:
    f.write("number\tpeople\n")
    for num, people in dreams.iteritems():
        f.write("%i\t%s\n" % (num, people.split('\t')[1]))
