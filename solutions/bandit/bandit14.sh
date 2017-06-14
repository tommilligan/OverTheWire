#!/bin/sh

# Read required input (current password)
cat /etc/bandit_pass/bandit14 | \

# Into a netcat connection (nc will automatically detect and connect telnet)
nc localhost 30000 | \

# Grep out the password in the response
egrep "\w{32}"

