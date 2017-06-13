django-tail
===========

利用django + channels 实现Liux tail -f 功能

## python requirement
python 2.7+ / 3.4+ is recommended

## 功能
用户登录后，可以查看在线日志。

## screenshot
![image](https://github.com/xianfuxing/django-tail/raw/master/static/images/sample.png)
## Installation
<pre>
<code>pip install django==1.10</code>
<code>pip install channels==1.1.3</code>
<code>pip install asgi-redis==1.4.0</code>
</pre>

## Getting Started
<pre>
<code>python manage.py makemigrations accounts</code>
<code>python manage.py migrate</code>
<code>python manage.py createsuperuser</code>
<code>python manage.py runserver</code>
</pre>

## Settings
Edit settings.py

<code>LOGTAIL_FILE = '/var/log/nginx/access.log'</code>

## To be continue...
1. ~~增加search功能，待续...~~ (done)
2. 增加click log line选中
