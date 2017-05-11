Web helpdesk interface
=====
[![Build Status](https://travis-ci.org/dvoraka/webrt.svg?branch=master)](https://travis-ci.org/dvoraka/webrt)

Web helpdesk interface using Django and [py-rt](https://github.com/dvoraka/py-rt) library. A simple interface with SSO for enterprise helpdesk solution [Request tracker](https://bestpractical.com/request-tracker/).

Logo file is named /static/logo.png and its size is 960x115 px.

Install helper:
https://raw.github.com/dvoraka/webrt/master/install_helper.sh

![](/imgs/login.png)
![](/imgs/afterlogin.png)
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
