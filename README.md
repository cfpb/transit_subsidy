# CFPB Labs - Transit Subsidy web application
<img src="transit_subsidy/master/transit_subsidy/static/images/screen_shot.png">

## Dependencies
 - nose test - http://readthedocs.org/docs/nose/en/latest/
 - django-nose - https://github.com/jbalogh/django-nose 


## Installation
 - Clone this repo ```$git clone https://github.com/cfpb/transit_subsidy```
 - Edit ```local_settings.py``` and edit the ```APP_ROOT``` property at the top of the
   file so that it matches your installation path.
 - Run ```$./manage.py runserver```
 - Open a web browser to  [http://localhost:8000/|http://localhost:8000/]
 - Log in using ted/ted for username and password
 - Access the Django admin: log out and log in as admin/admin


## Configuration

## Notes
 - Admin account info: username: admin, pwd: admin
 - Static assets!  Edit colorbox.css and templates to point to STATIC_URL



