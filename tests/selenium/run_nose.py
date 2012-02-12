#!/usr/bin/python

import os,io,json
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

# How to put this in a global scope?
# capability = get_capability( os.environ['browser'] )

nose.run( argv=['-s','-v'] )
