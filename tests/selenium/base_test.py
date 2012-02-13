import time, os,io,json, logging, inspect
from unittest import TestCase
from nose.tools import *
from nose import with_setup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os,io,json
import nose
from TransitSubsidyApp import TransitSubsidyApp



# create logger
logger = logging.getLogger('transit')
logger.setLevel(logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter('[%(name)s] %(asctime)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)



driver = None
transit = None
base_url = os.environ['site_under_test']

logger.info( 'Contacting hub at: %s' % os.environ['selenium_hub'] )




def zzz(secs=1):
    time.sleep(secs)


def handle_exception(driver, prefix, exception, test_results_dir='test-results/'):
    driver.get_screenshot_as_file( test_results_dir + prefix + '_error.png')
    html = open(test_results_dir + prefix + '_error.html' , 'w')
    html.write( driver.page_source.encode('utf-8') )
    html.close()
    print('\n')
    logger.error('Screenshot: http://cbdevsb01.cfpb.local:8080/jenkins/job/www-selenium/ws/cfpb/' + test_results_dir + prefix  + '_error.png')
    logger.error('HTML Source: http://cbdevsb01.cfpb.local:8080/jenkins/job/www-selenium/ws/cfpb/' + test_results_dir + prefix  + '_error.html')
    print('\n')
    raise  Exception(exception)


def is_textpresent(driver, text):
    ok_(  driver.page_source.find(text) ) 


def is_element_present(driver, how, what):
    try: driver.find_element(by=how, value=what)
    except NoSuchElementException, e: return False
    return True



def get_capability(browser):
    cfg_file = os.path.join(os.path.dirname(__file__), './selenium-config.json')
    f = open(cfg_file)
    data = f.read()
    # print data
    config = json.loads( data )
    for capability in config['capabilities']:
        if capability.keys()[0] == browser:
            return capability[capability.keys()[0]]
    
    raise Exception('Capability does not exist in ' )



#Put this somewhere else!
FF = {
            "platform": "ANY",
            "javascriptEnabled": True,
            "cssSelectorsEnabled": True,
            "handlesAlerts": True,
            "browserName": "firefox",
            "nativeEvents": False,
            "takesScreenshot": True,
            "version": ""
        }

FF36 = {
            "platform": "ANY",
            "javascriptEnabled": True,
            "cssSelectorsEnabled": True,
            "handlesAlerts": True,
            "browserName": "firefox",
            "nativeEvents": False,
            "takesScreenshot": True,
            "version": ""
        }

FF9 = {
            "platform": "ANY",
            "javascriptEnabled": True,
            "cssSelectorsEnabled": True,
            "handlesAlerts": True,
            "browserName": "firefox",
            "nativeEvents": False,
            "takesScreenshot": True,
            "version": "9"
        }

FF10 = {
            "platform": "ANY",
            "javascriptEnabled": True,
            "cssSelectorsEnabled": True,
            "handlesAlerts": True,
            "browserName": "firefox",
            "nativeEvents": False,
            "takesScreenshot": True,
            "version": "10"
        }


IE = {
            "platform": "ANY",
            "javascriptEnabled": True,
            "cssSelectorsEnabled": True,
            "handlesAlerts": True,
            "browserName": "internet explorer",
            "nativeEvents": False,
            "takesScreenshot": True,
            "version": ""
        }

CHROME = {
              "platform": "ANY",
              "javascriptEnabled": True,
              "acceptSslCerts": False,
              "browserName": "chrome",
              "rotatable": False,
              "locationContextEnabled": False,
              "databaseEnabled": False,
              "cssSelectorsEnabled": True,
              "handlesAlerts": True,
              "browserConnectionEnabled": True,
              "nativeEvents": True,
              "webStorageEnabled": False,
              "chrome.nativeEvents": False,
              "applicationCacheEnabled": False,
              "takesScreenshot": True
            }        



_browser = os.environ['browser'].upper()

logger.debug(_browser)

_capabilities = {}

if    _browser == 'IE':  _capabilities = IE
elif  _browser == 'INTERNET EXPLORER':    _capabilities = IE
elif  _browser == 'FIREFOX': _capabilities = FF
elif  _browser == 'FF': _capabilities = FF
elif  _browser == 'FF36': _capabilities = FF36
elif  _browser == 'FF9': _capabilities = FF9
elif  _browser == 'FF10': _capabilities = FF10
elif  _browser == 'CHROME' : _capabilities = CHROME
else:  _capabilities = FF9


logger.info( 'Capabilities: %s' % _capabilities )
print( '\n-------------------------------------\n')

def new_driver():
    _driver = webdriver.Remote( 
            command_executor=os.environ['selenium_hub'],
            desired_capabilities=_capabilities )
    _driver.implicitly_wait(5)
    return  _driver




         
