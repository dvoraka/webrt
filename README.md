Introduction
=====
Web interface using [py-rt](https://github.com/dvoraka/py-rt) library.

Logo file is named /static/logo.png and its size is 960x115 px.

Request tracker 4 Apache config on Debian. Add to your virtual host:
```
Include /etc/request-tracker4/apache2-modperl2.conf
RedirectMatch ^/$ /rt
```
