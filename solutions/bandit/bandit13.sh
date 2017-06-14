#!/bin/sh

# Move to a temporary directory
cd $(mktemp -d)

# Secure copy password file using bandit14's private key
# From the known location to our current directory
scp -i ~/sshkey.private -o StrictHostKeyChecking=no -P 2220 bandit14@localhost:/etc/bandit_pass/bandit14 .

# Once scp is completed read the resulting file
cat bandit14
