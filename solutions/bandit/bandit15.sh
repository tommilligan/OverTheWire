#!/bin/sh

# Read required input (current password)
cat /etc/bandit_pass/bandit15 | \

# Into a netcat connection (nc will automatically detect and connect telnet)
openssl s_client -connect localhost:30001 -ign_eof 2> /dev/null | \

# Grep out the password in the response
egrep "^\w{32}$"

