# natas5

On loading, the page tells us we are not logged in.

> These writeups assume you are using Google Chrome

Fire up DevTools (F12), and refresh the page. In the *Network* tab, we can see that the main page reponse headers include:
```
Set-Cookie: loggedin=0
```

We can set this to `1` in DevTools (*Application > Storage > Cookies*). Refreshing the page now gives us the password.

