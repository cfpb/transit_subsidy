#!/bin/bash

# Simple Python shell to run all the tests locates here (./tests)
# To Do: make mo better

echo '---------------------- Running Tests -----------------------'
echo ''
 ../manage.py test -s -v2 --with-xunit --with-coverage --cover-package=news,transit_subsidy,cards,services,ps,front,utils --cover-html --cover-html-dir=./coverage --cover-erase  ./
echo ''
echo '--------------------- End Test run ------------------------'
