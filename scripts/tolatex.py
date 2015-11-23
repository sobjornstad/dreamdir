# convert a range of dreams to LaTeX formatting
import os
import re
import sys

INPUT_DIRECTORY = '..'
fields = ('Id:\t', 'People:\t', 'Lcd:\t', 'Places:\t', 'Tags:\t', 'Date:\t')

def parseHeaders(headers):
    id, date = None, None
    try:
        for i in headers:
            if i.startswith('Id:\t'):
                id = i.split('\t')[1].strip()
            elif i.startswith('Date:\t'):
                date = i.split('\t')[1].strip()
    except:
        print "Invalid header format! Raising original error:"
        raise
    if not (id and date):
        print "Invalid header format (id and date not present)!"

    id = str(int(id)) # quick hack to get rid of leading zeroes
    year, month, day = date.split('-')
    year = year[2:]
    return id, (year, month, day)

def parseText(text):
    text = text.replace('&', '\\&')
    text = text.replace('#', '\\#')
    text = text.replace('%', '\\%')
    text = text.replace('$', '\\$')

    text = text.replace('{', '')
    text = text.replace('}', '')
    text = text.replace('...', '\elips ')

    # based off exporting.py in RPPAS
    text = re.sub("`(.*?)`", "\\dreamv{\\1}", text)
    text = re.sub("\*(.*?)\*", "\emph{\\1}", text)
    text = re.sub("_(.*?)_", "\emph{\\1}", text)
    text = re.sub("\"(.*?)\"", "``\\1''", text)
    # we could have typoes or other uses that result in single underscores
    text = text.replace('_', '\\textunderscore ')

    text = re.sub("([A-Z][A-Z][A-Z]*?) ", r"\\acro{\1} ", text)

    return text



##### MAIN #####
# let user input range
while True:
    start = raw_input("Start with dream #")
    end   = raw_input("Go through dream #")
    try:
        start = int(start)
        end = int(end)
    except ValueError:
        print "Entries not ints. Try again."
        continue
    else:
        break

# get appropriate filenames
rawL = os.listdir(INPUT_DIRECTORY)
l = [i for i in rawL if i.endswith('.dre')]
l.sort()
l = l[start-1:end]

ftexts = []
for dreamfile in l:
    with open(INPUT_DIRECTORY + "/" + dreamfile) as f:
        ftexts.append(f.readlines())

convertedtexts = []
for ft in ftexts: # for each girl :P
    headers = []
    line = 0 # prevent garbage collect: we want to know where the headers stop
    for line in range(len(ft)):
        if ft[line].startswith(fields):
            headers.append(ft[line])
        else:
            # end of headers
            break
    line = line + 1
    text = ''.join(ft[line:])
    text = parseText(text)
    id, date = parseHeaders(headers)
    dreamline = "\\dreamline{%s}{%s}{%s}{%s}" % (id, date[1], date[2], date[0])
    print dreamline
    print text
