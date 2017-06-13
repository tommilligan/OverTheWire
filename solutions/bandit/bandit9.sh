#!/bin/sh

# Get strings from binary file
strings data.txt | \

# Grep ones matching the description
egrep "^={8,}\s+\w{32}$" | \

# Throw away the leading equals signs
awk '{ print $2 }' 
