#!/usr/bin/python

import sys,os,io,json,subprocess
from os import popen
if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir
    path.append(dir(path[0]))

import nose


os.environ['http_proxy'] = 'http://127.0.0.1:4444' #http://127.0.0.1:4444
os.environ['selenium_hub'] = 'http://127.0.0.1:4444/wd/hub' 
os.environ['site_under_test'] = 'http://staging.consumerfinance.gov'
os.environ['google'] = 'http://google.com/'
os.environ['browser'] = 'Chrome'

#To Do: Start Selenium and Django here, then shut them down after test

nose.run( argv=['-s','-v'] )


