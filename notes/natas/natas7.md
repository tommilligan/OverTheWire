# natas7

The main page has a couple of links on. We can see clicking these passes a `page` parameter to the page `index.php`. Could this be an actual file path?

Navigating to `...?page=/etc/natas_webpass/natas8` gives us the password.

## Explanation

In this case, the parameter passed is an actual file location. The logic behind the page is something like:

* Look in the URL for a file name
* Look up this file on the server
* Display contents of the file on the web page

As the website is running as user `natas8`, we can ask it to access the password file on the server for us.

## Mitigation

This attack could be mitigated by using constants that are resolved into file paths on the server side, such as:

##### Known page

* Client:
    * I want page `42`
* Server:
    * Page `42` is `data.txt`
    * Read `data.txt`
    * Display contents in web page

##### Unknown page

* Client:
    * I want page `/etc/natas_webpass/natas8`
* Server:
    * Don't know that constant
    * Return code `400: Bad Request`

