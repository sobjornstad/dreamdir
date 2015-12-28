import os
import sys

INPUT_DIRECTORY = '/home/soren/current/dreams/'

def getAttribForAllDreams(attrib):
    """
    Given an /attrib/ (e.g., 'Id', 'People'), return a dict containing an
    element for each dream in the directory which has said id, keys showing
    the dream numbers and values the entire (unprocessed) attribute line.
    """
    rawL = os.listdir(INPUT_DIRECTORY)
    l = [i for i in rawL if i.endswith('.dre')]

    dreams = {}
    for dreamfile in l:
        attribline = ''
        with open(INPUT_DIRECTORY + "/" + dreamfile) as f:
            while True:
                line = f.readline().strip()
                if not line:
                    # EOF
                    break
                if line.startswith('Id:\t'):
                    did = line.split('\t')[1].strip()
                if line.startswith('%s:' % attrib):
                    attribline = line
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
    rawL = os.listdir(INPUT_DIRECTORY)
    l = [i for i in rawL if i.endswith('.dre')]

    dreams = []
    for dreamfile in l:
        with open(os.path.join(INPUT_DIRECTORY, dreamfile)) as f:
            for line in f:
                linetext = line.strip()
                if linetext.startswith('Id:\t'):
                    did = line.split('\t')[1].strip()
                if linetext.startswith('%s:' % attrib):
                    if tag in linetext:
                        dreams.append(_safeGetIntId(did))
                    break
    return sorted(dreams)



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
