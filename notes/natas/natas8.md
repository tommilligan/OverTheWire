# natas8

Again we are faced with a secret to find. Looking in the linked source file shows us an `$encodedSecret`, and that to encode new secrets the function is:
```
function encodeSecret($secret) {
    return bin2hex(strrev(base64_encode($secret)));
}
```

So to decode the secret, we will:

* Convert from hex
* to binary
* to string (ASCII)
* Reverse order of letters
* Base64 decode

and then put the secret back into the page form.

## Implementation

A great tool for challenges like this is [CyberChef](https://gchq.github.io/CyberChef/#recipe=%5B%7B%22op%22%3A%22From%20Hex%22%2C%22args%22%3A%5B%22Space%22%5D%7D%2C%7B%22op%22%3A%22To%20Binary%22%2C%22args%22%3A%5B%22Space%22%5D%7D%2C%7B%22op%22%3A%22From%20Binary%22%2C%22args%22%3A%5B%22Space%22%5D%7D%2C%7B%22op%22%3A%22Reverse%22%2C%22args%22%3A%5B%22Character%22%5D%7D%2C%7B%22op%22%3A%22From%20Base64%22%2C%22args%22%3A%5B%22A-Za-z0-9%2B%2F%3D%22%2Ctrue%5D%7D%5D)

