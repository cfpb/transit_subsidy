# Django settings for intra project.
import sys
from django.contrib.staticfiles import views
from settings import *
from django.conf.urls.defaults import patterns, include, url

#print sys.argv

if 'test' in sys.argv:
    # if 'test' is part of the comman then use sqlite3, else use mysql
    DATABASES = {
        'default': {
               'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
               'NAME': './sqlite_db/transit_subsidy_testing.db',                      # Or path to database file if using sqlite3.
               'USER': '',                      # Not used with sqlite3.
               'PASSWORD': '',                  # Not used with sqlite3.
               'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
               'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
               # 'TEST_NAME' : 'bills_test_database_of_death',
           },
        }
else:
    DATABASES = {
        'default': {
               'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
               'NAME': './sqlite_db/transit_subsidy.db',                      # Or path to database file if using sqlite3.
               'USER': '',                      # Not used with sqlite3.
               'PASSWORD': '',                  # Not used with sqlite3.
               'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
               'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            #'TEST_NAME' : 'bills_test_database_of_death',
        },
    }
    


DEPLOYED = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

#overriding settings.py ...?  Should be only during test?
AUTHENTICATION_BACKENDS = (
  'django.contrib.auth.backends.ModelBackend',
)

MANAGERS = ADMINS


# Works better than the Django default
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Where Django Test finds fixture data
FIXTURE_DIRS = (
  '/home/billy/webapps/transit_subsidy_os/tests/fixtures',
)

INSTALLED_APPS += ('django_nose','tests',)
# urlpatterns += ( url(r'^mobile/', 'mobile.views.index', ) )




# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
#STATIC_URL = '/tests/coverage/'


# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #('ps', '/var/www/django/intra/ps/static')
    #'/home/cfpb/william.shelton/webapps/collab/tests/coverage/',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''



TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #'/var/www/django/intra/templates/',
    '/home/billy/webapps/transit_subsidy_os/templates',
)




EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False

