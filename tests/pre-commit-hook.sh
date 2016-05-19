#!/bin/bash

echo "Running tests..."
tests/test_dr || exit 1

echo -e "\nRebuilding C code to check for errors..."
cd scripts
make clean
make || exit 1
cd - > /dev/null

echo -e "\nEverything completed successfully."
