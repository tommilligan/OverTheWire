#!/bin/sh

# Read file (appears to be a list of web bookmarks)
cat ~/.backup/bookmarks.html | \

# Search for anything to do with a password
grep password | \

# Strip out the password
sed -r 's/^.*password for leviathan1 is (\w+).*$/\1/'

