# natas2

Viewing the source, we see the following comment:
```
<!-- No more information leaks!! Not even Google will find it this time... -->
```

Google is a reference to the [robots.txt](https://en.wikipedia.org/wiki/Robots_exclusion_standard) file that many website uses. The file is a polite request to search engines (such as Google) of how to behave on the site.

However, any public content will remain public, `robots.txt` or not! If we navigate to `/robots.txt`, we see:

```
Disallow: /s3cr3t/
```

In `/s3cr3t` we again find the `users.txt` file which contains the password for `natas4`.

