#!/bin/sh

# Read source
cat /krypton/krypton1/krypton2 | \

# ROT13
tr A-Z N-ZA-M | \

# Get just password
awk '{ print $4 }'

