Introduction
=====
Web interface using [py-rt](https://github.com/dvoraka/py-rt) library.

Logo file is named /static/logo.png and its size is 960x115 px.

Install helper:
https://raw.github.com/dvoraka/webrt/master/install_helper.sh

#### Notes:

Debian Wheezy RT4 install:
```
aptitude install request-tracker4
```

Request tracker 4 Apache config on Debian. Add to your virtual host:
```
Include /etc/request-tracker4/apache2-modperl2.conf
RedirectMatch ^/$ /rt
```

It's probably better to use HTTPS if RT4 is not locally.

After install RT4:

* create queue and change settings.py
* add rights to queue
* create privileged user and change settings.py
