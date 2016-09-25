#!/usr/bin/env python2
"""
Regenerate a file of tags for Vim. Such a tags file allows you to follow
cross-references (if you write 'see #1000', you can put your cursor on 1000 and
press C-] to be taken to dream 1000), as well as to see other uses of header
values (in the line 'Tags: foo, bar baz', select the text 'bar baz' in visual
mode and press g]).

See the README for more information.
"""

import os
import ddirparse

OUTPUTFILE = os.path.join(ddirparse.DREAMDIR, '.dreams.ctags')

tags = []
headers = ddirparse.getAllHeaders()
for dream_id, headers in sorted(headers.iteritems()):
    tags.append((str(int(dream_id)), dream_id, "1"))
    title = headers.get('Title', '')
    for hname, hcontent in headers.iteritems():
        for part in hcontent.split(', '):
            tags.append((part, dream_id, '/%s:\t%s/%s' % (
                hname, hcontent, (' " || Title: %s' % title if title else ''))))

tags.sort(key=lambda i: str(i[0])) # tags files should be sorted
with open(OUTPUTFILE, 'w') as f:
    for tag, filenum, linenum in tags:
        f.write('%s\t%s\t%s\n' % (tag, "%s.dre" % filenum, linenum))
