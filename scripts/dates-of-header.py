# -*- coding: utf-8 -*-

import ddirparse

attrName = 'People'
timeBuckets = 20

dates = {k: v.split('Date:\t')[1]
         for k, v in ddirparse.getAttribForAllDreams('Date').iteritems()}
attrDict = ddirparse.getAttribForAllDreams('People')
dreamAttrs = {k: v.split(attrName + ':\t')[1].split(',')
         for k, v in attrDict.iteritems()}

#attrValueList = list(set([value.strip()
                     #for dream in dreamAttrs.items()
                     #for value in dream[1]]))

occurrencesByAttr = {}
for dream in dreamAttrs.items():
    dreamnum, valueList = dream
    for value in valueList:
        occurrencesByAttr[value.strip()] = \
                occurrencesByAttr.get(value.strip(), []) + [dreamnum]

# two-level sort: first level by frequency, second alphabetical
sortedValues = sorted(occurrencesByAttr.keys(), key=lambda i: i)
sortedValues.sort(key=lambda i: len(occurrencesByAttr[i]), reverse=True)


with open('header-on-dates.csv', 'w') as f:
    for attrValue, dreamnums in occurrencesByAttr.iteritems():
        f.write("%s,%s\n" % (attrValue,
                ' '.join((dates[dreamnum] for dreamnum in dreamnums))))

# TODO:
# We want to split the dates up into timeBuckets buckets, and provide information on how many observations were found in those. We then will have three variables, the attribute/person, the time bucket, and the number of observations in said time bucket. We'll need to repeat the attribute line several times in the output data if it takes place in multiple time buckets. Then we should be able to do a three-variable scatterplot in ggplot.
#
