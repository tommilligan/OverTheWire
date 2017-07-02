# natas6

The page looks like it takes a user secret as a form input, and checks it server-side. We are helpfully given the source code (PHP), which contains:
```
include "includes/secret.inc";

if(array_key_exists("submit", $_POST)) {
    if($secret == $_POST['secret']) {
        ...
    }
    ...
}
```

From this we can guess the variable `$secret` is specified in `includes/secret.inc`. Navigating there gives us the secret - feeding this back into the original form gives us the password.

