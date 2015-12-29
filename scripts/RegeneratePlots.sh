#!/bin/bash

python ./date-dotplot.py
R --vanilla < ./date-dotplot.R
rm dotplot-data.csv

rm -f Rplots.pdf
