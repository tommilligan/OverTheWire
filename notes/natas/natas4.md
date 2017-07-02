# natas4

On first visiting the site, we see a warning saying we are not visiting from the URL for `natas5`. Normally, clicking on an URL to a page casues the client's web browser to set the `Referer` header, so the incoming page knows where the client has just been.

However, as the client provides this information, we can set out own value. There are many apps/extensions that can do this ([Postman](https://www.getpostman.com/) is good) - however the simplest way is just to use cURL from the command line:
```
curl \
-H "Referer: http://natas5.natas.labs.overthewire.org/" \
-X GET 'http://natas4:Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ@natas4.natas.labs.overthewire.org/' | \

grep natas5
```

