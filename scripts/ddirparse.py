# -*- coding: utf-8 -*-

"""
ddirparse Python library

This module provides several convenient functions for pulling data from dreams
in the dreamdir format. It is used in 'dr' and provided dreamdir scripts and is
also appropriate for user scripts.
"""

import os
import sys

DREAMDIR = '/home/soren/current/dreams/'

def getAttribForAllDreams(attrib):
    """
    Given an /attrib/ (e.g., 'Id', 'People'), return a dict containing an
    element for each dream in the directory which has said id, keys showing
    the dream numbers and values the entire (unprocessed) attribute line.
    """

    dreams = {}
    for f in allDreamfiles():
        attribline = ''
        did = None
        for line in f:
            textline = line.strip()
            if textline.startswith('Id:\t'):
                did = textline.split('\t')[1].strip()
            if textline.startswith('%s:' % attrib):
                attribline = textline
                break

        if not did:
            print "ERROR: Missing id in a dream file!"
            sys.exit(1)
        if not attribline:
            continue
        did = _safeGetIntId(did)
        dreams[did] = attribline

    return dreams

def getDreamsTagged(attrib, tag):
    """
    Find all dreams that are tagged with 'tag' as one of the 'attrib'
    attributes.
    """
    dreams = []
    for f in allDreamfiles():
        for line in f:
            linetext = line.strip()
            if linetext.startswith('Id:\t'):
                did = line.split('\t')[1].strip()
            if linetext.startswith('%s:' % attrib):
                if tag in linetext:
                    dreams.append(_safeGetIntId(did))
                break
    return sorted(dreams)


def allDreamfiles():
    """
    Generator function for iterating over all dreamfiles in the directory.

    Example (prints the contents of the dreamdir to stdout):
    >>> for f in allDreamfiles():
    >>>     for line in f:
    >>>         print(line)
    """
    listing = os.listdir(DREAMDIR)
    for dreamfile in (i for i in listing if i.endswith('.dre')):
        with open(os.path.join(DREAMDIR, dreamfile)) as f:
            yield f



### Private helper functions ###
def _safeGetIntId(did):
    """
    Throw a useful error if a dreamfile has a non-integer ID number.
    """
    try:
        return int(did)
    except ValueError:
        print "ERROR: Non-integer id (%s) in a dream file!" % did
        raise
