#!/bin/bash

# Simple Python shell to run all the tests ( The Hood should do this)

echo '---------------------------- Running Unit Tests ------------------------------'
echo ''
 ../manage.py test --exclude=selenium --include=transit_subsidy -s -v2 --with-xunit --with-coverage --cover-package=transit_subsidy --cover-html --cover-html-dir=./coverage --cover-erase  ./


# ../manage.py test --exclude=selenium --include=transit_subsidy -s -v2 

echo '--------------------------- Running Selenium Tests ---------------------------------'

cd selenium
./run_nose.py 

echo ''
echo '-------------------------- End Test run ------------------------------------'
