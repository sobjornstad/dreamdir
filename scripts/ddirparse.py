# -*- coding: utf-8 -*-

"""
ddirparse Python library

This module provides several convenient functions for pulling data from dreams
in the dreamdir format. It is used in 'dr' and provided dreamdir scripts and is
also appropriate for user scripts.
"""

import os
import re
import sys

DREAMDIR = os.getenv("DREAMDIR") # None if not set

def setDreamdir(path):
    """
    Specify a non-standing and non-environment-variable value for the
    dreamdir location, to persist for the remainder of the module's lifetime
    unless changed again.
    """
    global DREAMDIR
    DREAMDIR = path


### General tools ####
def strHighlight(s, colors):
    """
    Interpolate the terminal coloring codes specified in colorDict into the
    string 's' based on dreamdir syntax rules.

    The string should contain headers, and may also contain dream text.

    colorDict should specify color codes as the values for keys 'headers',
    'lucid', 'notes', and 'verbatim', and the clear code for the key 'clear'.
    These can be obtained with, e.g., tput(1).
    """
    out = []
    charColors = {'{': 'lucid', '[': 'notes', '\`': 'verbatim'}
    try:
        headers, rest = s.split('\n\n', 1)
    except ValueError:
        # nothing provided beyond the headers, or input is malformed
        headers = s
        rest = ''

    for i in headers.split('\n'):
        out.append(re.sub(r'^(.*):\t(.*)$',
                          r'%s\1:\t%s\2' % (colors['headers'], colors['clear']),
                          i))
        out.append('\n')
    out.append('\n')

    colStack = []
    curColor = colors['clear']
    inBacktick = False
    for char in rest:
        if char in ('[', '{') or (char == '\`' and not inBacktick):
            colStack.append(curColor)
            curColor = colors[charColors[char]]
            out.append(curColor)
            out.append(char)
        elif char in (']', '}') or (char == '\`' and inBacktick):
            out.append(char)
            curColor = colStack.pop()
            out.append(curColor)
        else:
            out.append(char)
        if char == '\`':
            inBacktick = not inBacktick
    return ''.join(out)

def allDreamfiles():
    """
    Generator function for iterating over all dreamfiles in the directory.

    Example (prints the contents of the dreamdir to stdout):
    >>> for f in allDreamfiles():
    >>>     for line in f:
    >>>         print(line)
    """
    if not DREAMDIR:
        print "Error: Dreamdir not specified! To fix this error, use the"
        print "setDreamdir() function after importing this module, or set the"
        print "DREAMDIR environment variable."
        sys.exit(1)

    listing = os.listdir(DREAMDIR)
    for dreamfile in (i for i in listing if i.endswith('.dre')):
        with open(os.path.join(DREAMDIR, dreamfile)) as f:
            yield f

### Dream headers ###
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
            if not textline: # blank line indicates end of headers
                break
            if textline.startswith('Id:\t'):
                did = textline.split('\t')[1].strip()
            if textline.startswith('%s:\t' % attrib):
                attribline = textline

        if not did:
            print "ERROR: Missing id in dream file %s!" % f.name
            sys.exit(1)
        if not attribline: # dream doesn't have the specified attribute at all
            continue
        did = _safeGetIntId(did)
        dreams[did] = attribline

    return dreams

def getAllHeaders():
    dreams = {}
    for f in allDreamfiles():
        dream = {}
        for line in f:
            if not line.strip(): # end of headers
                break
            header, value = (i.strip() for i in line.split(':\t'))
            dream[header] = value
        dreams[dream['Id']] = dream
    return dreams

def getDreamsTagged(attrib, tag):
    """
    Find all dreams that are tagged with 'tag' as one of the 'attrib'
    attributes.
    """
    dreams = []
    attribDict = getAttribForAllDreams(attrib)
    for dream, attribline in attribDict.iteritems():
        content = [i.strip() for i in attribline.split('\t')[1].split(',')]
        for contentItem in content:
            if re.match(tag, contentItem) is not None:
                dreams.append(_safeGetIntId(dream))
                break
    return sorted(dreams)


##### Word count #####
# Our word count is superior to standard utilities because it ignores headers
# and can split the word count into normal, lucid, and notes portions. It's
# certainly slower, but in my testing it took only about 1.7ms per file.

def countFile(f):
    """
    Count words in file f, ignoring headers entirely and splitting word count
    into normal, lucid, and notes (bracketed) portions.
    """
    words = {'normal': 0, 'lucid': 0, 'notes': 0}
    flags = {'inHeaders': True, 'inLucid': False, 'inNotes': False}
    inWord = False
    for line in f:
        # skip ahead until we get to the end of the headers
        if flags['inHeaders']:
            if not line.strip():
                flags['inHeaders'] = False
            continue

        for char in line:
            if re.match(r"[\w']", char):
                if not inWord: # we just started a word, inc count
                    if flags['inNotes']:
                        words['notes'] += 1
                    elif flags['inLucid']:
                        words['lucid'] += 1
                    else:
                        words['normal'] += 1
                inWord = True
            else: # leave word
                inWord = False

            if char == "[":
                flags['inNotes'] = True
            elif char == "]":
                flags['inNotes'] = False
            elif char == "{":
                flags['inLucid'] = True
            elif char == "}":
                flags['inLucid'] = False
    return words

def countAll():
    """
    Sum word counts of all files in the dreamdir. See note in getCount()
    docstring about performance.
    """
    words = {'normal': 0, 'lucid': 0, 'notes': 0}
    for i in allDreamfiles():
        for k, v in countFile(i).iteritems():
            words[k] += v
    return words

def getCount(filenames=None, normal=True, lucid=True, notes=True, total=True,
             asString=False, asPrettyString=False):
    """
    Get summed count of a list of filenames.

    Note that this is slow as molasses in January over a large dreamdir. A C
    implementation is available, scripts/drwc.c, which can be compiled into
    scripts/bin/drwc using the included Makefile (if you have gcc installed).
    This implementation runs over 10 times faster, though it doesn't know how
    to handle multibyte characters and may thus result in slightly different
    values.
    """
    words = {'normal': 0, 'lucid': 0, 'notes': 0}
    if filenames is None:
        words = countAll()
    else:
        for file in filenames:
            for k, v in countFile(open(file)).iteritems():
                words[k] += v
    words['total'] = sum(count for type, count in words.iteritems())

    doReturn = [field for include, field
                in zip((normal, lucid, notes, total),
                       ('normal', 'lucid', 'notes', 'total'))
                if include]
    if asString:
        return ' '.join(str(words[i]) for i in doReturn)
    elif asPrettyString:
        return '\n'.join(["%s:\t%s" % (i.title(), words[i])
                         for i in ('normal', 'lucid', 'notes', 'total')
                         if i in doReturn])
    else:
        return {k:v for k,v in words.iteritems() if k in doReturn}


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
