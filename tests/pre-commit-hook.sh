#!/bin/bash

# requires shellcheck: http://www.shellcheck.net/
echo -n "Running shellcheck..."
shellcheck dr || exit 1
echo "OK"

# requires BATS: https://github.com/sstephenson/bats
# set CDPATH to nothing to work around a strange issue:
#     https://github.com/sstephenson/bats/issues/104
echo "Running tests..."
CDPATH='' tests/test_dr || exit 1
echo "OK"

# requires GCC or equivalent compiler with c99 support
echo -e "\nRebuilding C code to check for errors..."
{
cd drwc || exit 2
make clean
make || exit 1
}
echo "OK"

echo -e "Everything completed successfully."
