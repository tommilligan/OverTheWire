#!/bin/sh

# Decode base64 to ASCII 
base64 -d ~/data.txt | \

# Strip to bare password
awk '{ print $4 }'
