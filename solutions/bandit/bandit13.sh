#!/bin/sh

# Secure copy password file using bandit14's private key
# From the known location to our current home directory
# Once scp is completed read the resulting file
scp -i sshkey.private -P 2220 bandit14@localhost:/etc/bandit_pass/bandit14 ~ && cat ~/bandit14
