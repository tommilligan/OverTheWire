#!/bin/sh

# List all files in filesystem recursively, one line at a time.
# Throw away errors
ls -laR1 / 2> /dev/null | \

# Find file name from description at http://overthewire.org/wargames/bandit/bandit7.html
egrep "bandit7 +bandit6 +33" | \

# Pull out just the filename from the long description
sed -r "s/^.* ([^ ]+)/\1/" | \

# Find file path from filename
while read fileName; do
    find / -type f -name "$fileName" 2> /dev/null | \
    # Cat
    while read filePath; do
        cat "$filePath";
    done
done
