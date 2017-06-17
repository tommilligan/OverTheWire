#!/bin/sh

# ls -la ~
# file ~/check

# There is a binary (~/check) which leviathan1 can run
# The binary has permissons of leviathan2 which we can
# use to read the next level's password file

# ./check
# ^C

# The binary asks for a password when run
# strings rips out strings from a binary file

# strings ~/check

# Strings shows us 'password' and '/bin/sh'
# Hopefully if we guess the password we get a shell!
# We can also make out 'secret' ('secr' and 'et') near each other

# xxd ~/check | less

# Hexdumping allows a clearer look at what strings found
# Near 'secret' we can make out several strings (lines 0000540-60)
# sex, secreat, god, love

# sex it is
