import os
import sys

INPUT_DIRECTORY = '..'

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
        try:
            did = int(did)
        except ValueError:
            print "ERROR: Non-integer id (%s) in a dream file!" % did
        dreams[did] = attribline

    return dreams
