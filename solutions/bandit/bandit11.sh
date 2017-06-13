#!/bin/sh

# Read data file
cat ~/data.txt | \

# ROT13 cipher 
tr a-zA-Z n-za-mN-ZA-M | \

# Strip to bare password
awk '{ print $4 }'
