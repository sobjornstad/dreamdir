#!/usr/bin/env python2
# Create a LaTeX-formatted index of all the headers, to be \input in a skeleton
# file for fancy printing. I really like this format for reflecting on all the
# dreams I've had over a period of time.

import re
import ddirparse as dp
import pprint

PLOPPATH_HEADERS = '/home/soren/current/dreams/old/headerdex/content.tex'
PLOPPATH_INDEX = '/home/soren/current/dreams/old/headerdex/index-of-%s.tex'
indexHeaders = ('Tags', 'People', 'Places', 'Title')

def munge_latex(s):
    "Escape characters reserved by LaTeX in string s."

    s = s.replace('\\', '\\textbackslash ')
    s = s.replace('{', '\\{')
    s = s.replace('}', '\\}')
    s = s.replace('$', '\\$')
    s = s.replace('&', '\\&')
    s = s.replace('#', '\\#')
    s = s.replace('~', '\\textasciitilde ')
    s = s.replace('%', '\\%')

    # TODO: Fix this regex so it doesn't get mixed up if two people on a dreamline have a '*' in them (probably terminating the check at commas will do)
    # Italicize text-file emphasis.
    s = re.sub(r'\*(.*?)\*', r'\emph{\1}', s)
    s = re.sub(r'_(.*?)_', r'\emph{\1}', s)
    s = s.replace('_', '\\textunderscore ') # for any others

    # Take care of double straight quotation marks. Note that it's not possible
    # to handle single quotation marks correctly, as there's no way to tell if
    # it's an apostrophe or opening single quote. If you want it right with
    # singles, you need to use curlies in the original poem.
    s = re.sub('"(.*?)"', "``\\1''", s)

    # Clean up ellipses.
    s = s.replace('...', '\\elips ')

    # daggerify
    s = s.replace('+', '$\\dagger$')

    return s

allHeaders = dp.getAllHeaders()
txt = []
for dream, headers in sorted(allHeaders.iteritems()):
    addheads = []
    for k, v in sorted(headers.iteritems()):
        if k not in ('Title', 'Id', 'Date'):
            addheads.append("\n  \\setheader{%s}{%s}" % (k, munge_latex(v)))
    id = int(dream) # remove leading zeroes
    txt.append("\\setdream{%i}{%s}{\mbox{%s}}{%s}" % (
               id, headers['Date'], munge_latex(headers['Title']),
               ''.join(addheads) + '\n'))

with open(PLOPPATH_HEADERS, 'w') as f:
    f.write('\n\n'.join(txt))
    f.write('\n')

index = {} # headerDict
for dreamNum, dreamHeaders in allHeaders.iteritems():
    for header, valueForDream in sorted(dreamHeaders.iteritems()):
        thisHeaderVals = index.get(header, {})
        for unit in (i.strip() for i in valueForDream.split(',')):
            thisHeaderVals[unit] = thisHeaderVals.get(unit, []) + [int(dreamNum)]
        index[header] = thisHeaderVals


for headerName, content in (i for i in index.iteritems() if i[0] in indexHeaders):
    indexText = []
    for tag, dreams in sorted(content.iteritems(), key=lambda i: i[0].lower()):
        indexText.append("\\item {%s}, %s" % (
                             munge_latex(tag),
                             ', '.join(str(i) for i in sorted(dreams))))
    with open(PLOPPATH_INDEX % headerName.lower(), 'w') as f:
        f.write('\n'.join(indexText))
