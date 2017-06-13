#!/bin/sh

find ~/inhere/ -type f | while read i; do
    cat "$i" | egrep "^[a-zA-Z0-9]{32}$"
done 
