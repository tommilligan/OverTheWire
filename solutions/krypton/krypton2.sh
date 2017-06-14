#!/bin/sh

# Setup working area
cd $(mktemp -d)
ln -s /krypton/krypton2/keyfile.dat
chmod 777 .

# Cipher the alphabet
echo 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' > alphabet
/krypton/krypton2/encrypt alphabet

# Use the output file (ciphertext) to backtranslate
cat /krypton/krypton2/krypton3 | tr $(cat ciphertext) $(cat alphabet)

