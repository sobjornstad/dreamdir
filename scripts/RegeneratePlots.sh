#!/bin/bash
. ~/bin/common.sh

reason="Please run this script from the dreamdir root directory."
ensure '-d scripts' "$reason"
ensure '-d graphs'  "$reason"
ensure '-f dr'      "$reason"
pushd scripts

python ./date-dotplot.py
R --vanilla < ./date-dotplot.R

rm dotplot-data.csv
rm -f Rplots.pdf
popd
