#!/bin/sh

# Reverse hexdump file
xxd -r ~/data.txt - | \

# Unwind compression
gzip -dc | \
bzip2 -dc | \
gzip -dc | \
tar -xO | \
tar -xO | \
bzip2 -dc | \
tar -xO | \
gzip -dc | \

# Strip to bare password
awk '{ print $4 }'
