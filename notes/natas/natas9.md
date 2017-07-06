# natas9

## Analysis

Inspecting the source code, we can this web page allows us to complete a bash command with user input `$key`. The expression is then executed by the server (good ol' PHP).
```
passthru("grep -i $key dictionary.txt");
```

As the user input is not validated or cleaned in any way, we can simply fill in the blank with our own bash command!

## Implementation

A few notes:

* Can the existing command do what you want?
* You'll probably want to ignore everthing **after** your section of the command

A couple of working examples are shown below:

|idea|`$key`|
|-|-|
|Whole new command|`|| cat /etc/natas_webpass/natas10 #`
|Completing the grep command|`".*" /etc/natas_webpass/natas10 #`|


