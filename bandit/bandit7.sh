#!/bin/sh

# Grep data file for the given keyword
grep "millionth" data.txt | \

# Throw away the first column and return the second
sed -r "s/^\w+\s+(\w+)$/\1/"

