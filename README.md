Zip Sender Script
==================

![alt text](https://img.shields.io/badge/python-3.6-green.svg "Python3.6")

This script is executed on a daily basis, zips and sends via email all the files located in a specific directory that with a conditional pattern.
Dependecies:
-------------

Only built-in packages are used

How to start:
-------------

* Choose a folder to listen on
* Choose an SMTP server
* Set your Login Credentials if there's any
* Set the Sender Email Address and the Recipient Email
* Set the Subject and the content of the email
* Run $ pythonw zip_and_send.py
* Add this call to your crontab(unix)/task scheduler(windows) (or something similar) to check for changes regularly

Compatibility
-------------

Compatible with Python 3.x ,tested  on Python 3.6.
