#!/bin/bash

# Simple Python shell to run all the tests locates here (./tests)
# To Do: make mo better

echo '---------------------------- Running Tests ------------------------------'
echo ''
 ../manage.py test --exclude=selenium --include=transit_subsidy -s -v2 --with-xunit --with-coverage --cover-package=transit_subsidy --cover-html --cover-html-dir=./coverage --cover-erase  ./
 
echo '--------------------------- Selenium Tests ---------------------------------'

cd selenium
 ./run_nose.py
 

echo ''
echo '-------------------------- End Test run ------------------------------------'
