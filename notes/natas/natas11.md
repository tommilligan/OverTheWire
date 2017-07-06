# natas11

## Analysis

From the sourcecode, we can see when we enter a color, we will receive a XOR encrypted cookie with both `bgcolor` and `showpassword` data.
```
$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");

function xor_encrypt($in) {
    $key = '<censored>';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    } 

    return $outText;
}

function loadData($def) {
    global $_COOKIE;
    $mydata = $def;
    if(array_key_exists("data", $_COOKIE)) {
    $tempdata = json_decode(xor_encrypt(base64_decode($_COOKIE["data"])), true);
    if(is_array($tempdata) && array_key_exists("showpassword", $tempdata) && array_key_exists("bgcolor", $tempdata)) {
        if (preg_match('/^#(?:[a-f\d]{6})$/i', $tempdata['bgcolor'])) {
        $mydata['showpassword'] = $tempdata['showpassword'];
        $mydata['bgcolor'] = $tempdata['bgcolor'];
        }
    }
    }
    return $mydata;
}

function saveData($d) {
    setcookie("data", base64_encode(xor_encrypt(json_encode($d))));
}
```

## XOR

XOR is an operation that acts as reversible encryption. We can find the third component from either of the other two:

* PLAIN `XOR` KEY = CYPHER
* CYPHER `XOR` KEY = PLAIN
* PLAIN `XOR` CYPHER = KEY

In this case, we have control of the plaintext (user input) and receive the cyphertext (cookie). Therefore, we must be able to infer the key.

Submitting a color of `#888888`, we can see in DevTools we receive a cookie header:
```
Set-Cookie: data=ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSTwBySU8AaAw%3D
```

We can also see the current cookies in the DevTools console:
```
document.cookie
# "data=ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSTwBySU8AaAw%3D"
```

As the sourcecode shows us, this is simply a base64 encoding of the XOR'd JSON object.

Let's set a few colors and see what we get:

|Color input|Cookie `data`|
|-|-|
|#888888|ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhS**TwBySU8A**aAw|
|#ff8800|ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhS**EV5ySUcI**aAw|
|#0088ff|ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhS**RwhySRFe**aAw|

We can easily see the final section of the base64 encoding is changing due to our input. If this is where `bgcolor` is stored, we can infer the exact JSON layout, and use it to find `$key`.

```
# Cyphertext
ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSTwBySU8AaAw

# Known JSON structure
# {"showpassword":"no","bgcolor":"#888888"}
eyJzaG93cGFzc3dvcmQiOiJubyIsImJnY29sb3IiOiIjODg4ODg4In0

# XOR together to get key
qw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jq
```

> [Cyberchef implementation](https://gchq.github.io/CyberChef/#recipe=%5B%7B%22op%22%3A%22From%20Base64%22%2C%22args%22%3A%5B%22A-Za-z0-9%2B%2F%3D%22%2Ctrue%5D%7D%2C%7B%22op%22%3A%22XOR%22%2C%22args%22%3A%5B%7B%22option%22%3A%22UTF8%22%2C%22string%22%3A%22%7B%5C%22showpassword%5C%22%3A%5C%22no%5C%22%2C%5C%22bgcolor%5C%22%3A%5C%22%23888888%5C%22%7D%22%7D%2C%22Standard%22%2Cfalse%5D%7D%5D&input=Q2xWTEloNEFTQ3NDQkU4bEF4TWFjRk1aVjJoZFZWb3RFaGhVSlFOVkFtaFNUd0J5U1U4QWFBdw)

This matches the sourcecode - the PHP asks for the XOR key to repeat if the plaintext is longer than it.

# Exploitation

Now we know the key, we can form our own valid cookie:
```
# Desired JSON structure
# {"showpassword":"yes","bgcolor":"#ff8800"}
eyJzaG93cGFzc3dvcmQiOiJ5ZXMiLCJiZ2NvbG9yIjoiI2ZmODgwMCJ9

# Known key
# Note this is extended (repeated) to cover the length of our output base64
qw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw

# Our exploit cookie
ClVLIh4ASCsCBE8lAxMacFMOXTlTWxooFhRXJh4FGnBTVF4sSU8IelMK
```

> [Cyberchef implementation](https://gchq.github.io/CyberChef/#recipe=%5B%7B%22op%22%3A%22XOR%22%2C%22args%22%3A%5B%7B%22option%22%3A%22UTF8%22%2C%22string%22%3A%22%7B%5C%22showpassword%5C%22%3A%5C%22yes%5C%22%2C%5C%22bgcolor%5C%22%3A%5C%22%23ff8800%5C%22%7D%22%7D%2C%22Standard%22%2Cfalse%5D%7D%2C%7B%22op%22%3A%22To%20Base64%22%2C%22args%22%3A%5B%22A-Za-z0-9%2B%2F%3D%22%5D%7D%5D&input=cXc4SnF3OEpxdzhKcXc4SnF3OEpxdzhKcXc4SnF3OEpxdzhKcXc4SnF3)

Again, we can set this cookie just using DevTools:

```
document.cookie="data=ClVLIh4ASCsCBE8lAxMacFMOXTlTWxooFhRXJh4FGnBTVF4sSU8IelMK%3d"
```

Refreshing the page, we are given the password for `natas12`.