#!/usr/bin/python2

import ddirparse

##### http://stackoverflow.com/questions/2526815/moon-lunar-phase-algorithm
import datetime
import ephem

def get_phase_on_day(year,month,day):
  """Returns a floating-point number from 0-1. where 0=new, 0.5=full, 1=new"""
  #Ephem stores its date numbers as floating points, which the following uses
  #to conveniently extract the percent time between one new moon and the next
  #This corresponds (somewhat roughly) to the phase of the moon.

  #Use Year, Month, Day as arguments
  date=ephem.Date(datetime.date(year,month,day))

  nnm = ephem.next_new_moon    (date)
  pnm = ephem.previous_new_moon(date)

  lunation=(date-pnm)/(nnm-pnm)

  #Note that there is a ephem.Moon().phase() command, but this returns the
  #percentage of the moon which is illuminated. This is not really what we want.

  return lunation
##### End code copied from StackOverflow

wcs = {}
for f in ddirparse.allDreamfiles():
    date = None
    counting = False
    for line in f:
        textline = line.strip()
        if counting:
            wcs[date] += len(textline.split())
        else:
            if textline.startswith('Date:\t'):
                date = textline.split(':\t')[1].strip()
            elif not textline:
                # end of headers, start counter
                counting = True
                if date not in wcs:
                    wcs[date] = 0

lucids = ddirparse.getDreamsTagged('Lucid', '')
dreamToDate = {k: v.split(':\t')[1].strip()
               for k,v in ddirparse.getAttribForAllDreams('Date').iteritems()}
days = {k:{'wc':v} for k,v in wcs.iteritems()}
for day in days:
    days[day]['moon'] = get_phase_on_day(*[int(i) for i in day.split('-')])
    days[day]['lucid'] = 0
for ld in lucids:
    days[dreamToDate[ld]]['lucid'] = 1

with open("moonexperiment.csv", 'w') as f:
    f.write("Date\tLucidity\tWord count\tMoon\n")
    for date, info in sorted(days.iteritems()):
        f.write("%s\t%i\t%i\t%f\n" % (date, info['lucid'],
                                      info['wc'], info['moon']))

