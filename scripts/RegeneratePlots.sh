#!/bin/bash
# This script should place a graph in the graphs/ dreamdir subdirectory for all
# graphs there are scripts to create. Graph creation is normally handled by a
# Python script that pulls the data using 'ddirparse' and, if desired, an R
# script that plots the data.

. ~/bin/common.sh 1

reason="Please run this script from the dreamdir root directory."
ensure '-d scripts' "$reason"
ensure '-d graphs'  "$reason"
ensure '-f dr'      "$reason"
pushd scripts

echo -n "Tabulating dream dates..."
python ./date-dotplot.py
echo -e "done.\nGraphing data..."
R --vanilla --slave < ./date-dotplot.R

echo -n "Cleaning up..."
rm dotplot-data.csv
rm -f Rplots.pdf
popd
echo "done."
