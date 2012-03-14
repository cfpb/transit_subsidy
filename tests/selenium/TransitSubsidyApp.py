__author__ = 'CFPB Labs'

import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from nose.tools import *


class TransitSubsidyApp():
    """
        Abstration of the Transit Subsidy application.  This extends the
        WebDriver Page model pattern (http://code.google.com/p/selenium/wiki/PageObjects)
        and applies to the application as a whole rather than a single page state.

        @note_to_self: one or more page objects could comprise a application object, which,
                      more or less, could serve as a testing facade.

    """


    def __init__(self,driver,base_url):
        self.driver = driver
        self.base_url = base_url

    
    def reset(self):
        self.driver.find_element_by_link_text('Reset Form').click()


    def login(self, username="ted", password="ted" ):
        self.driver.get( self.base_url + "/login/")
        eq_("Your Intranet >", self.driver.title)
        self.driver.find_element_by_id("id_username").clear()
        self.driver.find_element_by_id("id_username").send_keys(username)
        self.driver.find_element_by_id("id_password").clear()
        self.driver.find_element_by_id("id_password").send_keys(password)
        self.driver.find_element_by_id("btn_login").click()
        eq_("Your Intranet > Transit Subsidy Request", self.driver.title)
     

    def logout(self):
        driver.get(base_url + "/logout/")    


    def commute_from( self, street='123 Main St', city='Anytown', state="VA", zip="62312" ):
        self.driver.find_element_by_id("id_origin_street").clear()
        self.driver.find_element_by_id("id_origin_street").send_keys(street) 
        self.driver.find_element_by_id("id_origin_city").clear()
        self.driver.find_element_by_id("id_origin_city").send_keys(city)
        self.driver.find_element_by_id("id_origin_state").clear()
        self.driver.find_element_by_id("id_origin_state").send_keys(state)
        self.driver.find_element_by_id("id_origin_zip").clear()
        self.driver.find_element_by_id("id_origin_zip").send_keys(zip)
    

    def commute_to(self, destination_id=2):
        self.driver.find_element_by_id("id_destination").find_elements_by_tag_name('option')[destination_id].click()

    
    def add_segment(self, segment_id,mode_id,amount,add_another=False):
        self.driver.find_element_by_id("segment-type_%s" % segment_id).find_elements_by_tag_name('option')[mode_id].click()
        self.driver.find_element_by_id("segment-amount_%s" % segment_id).clear()
        self.driver.find_element_by_id("segment-amount_%s" % segment_id).send_keys(amount)
        if add_another: self.driver.find_element_by_id("add_%s" % segment_id).click()
    

    def add_other_segment(self, segment_id, other_text, amount, add_another=False):
        self.driver.find_element_by_id("segment-type_%s" % segment_id).find_elements_by_tag_name('option')[17].click()
        time.sleep(1)
        self.driver.find_element_by_id("segment-other_%s" % segment_id).send_keys(other_text)
        self.driver.find_element_by_id("segment-amount_%s" % segment_id).clear()
        self.driver.find_element_by_id("segment-amount_%s" % segment_id).send_keys(amount)
        if add_another: self.driver.find_element_by_id("add_%s" % segment_id).click()
    
    def remove_segment(self,segment_id):
        self.driver.find_element_by_id('rm_%s' % segment_id).click()
     
    def click_add(self):
        self.driver.find_element_by_id('add_1').click()    
    

    def select_workdays(self, id=2, other=None):
        self.driver.find_element_by_xpath("(//input[@id='id_work_sked'])[%s]" % id).click()
        if id==4: 
            self.driver.find_element_by_id('id_number_of_workdays').clear() 
            self.driver.find_element_by_id('id_number_of_workdays').send_keys(other)


    def view_smartriphelp(self):
        self.driver.find_element_by_id("id_help_smartrip").click()
        #Keys.ESCAPE should work, too
        self.driver.find_element_by_id("cboxClose").click()


    def add_smartrip(self, num='00020 0001 5644 364 6'):
        self.driver.find_element_by_id("id_dc_wmta_smartrip_id").clear()
        self.driver.find_element_by_id("id_dc_wmta_smartrip_id").send_keys(num)
    

    def enroll(self):
        time.sleep(.5)
        self.driver.find_element_by_id("btn_enroll_smartrip").click()
        time.sleep(1)

    
    def sign(self, last_four_ssn='1234', signature='Mick Jagger'):    
        time.sleep(.5)
        self.driver.find_element_by_id("id_last_four_ssn").send_keys(last_four_ssn)
        self.driver.find_element_by_id("id_signature").send_keys(signature)
        self.driver.find_element_by_id("btn_agree").click()
        time.sleep(.5)
        eq_("Your Intranet > Transit Subsidy Confirmation", self.driver.title)

    
    def dont_sign(self):    
        self.driver.find_element_by_id("btn_no_agree").click()
        eq_("Your Intranet > Transit Subsidy Request", self.driver.title)

    
    def withdraw_enrollment(self):
        
        # Running out of time this morning. This aint workin!
        # self.driver.find_element_by_link_text('Cancel my enrollment.').click()
        #test no agree (for grins)
        # time.sleep(.5)
        # self.driver.find_element_by_id("btn_withdraw_no_agree").click()
        #Selenium thowing Element is not clickable at point (558, 165). Other element would receive the click: <div id="cboxOverlay" style="cursor: pointer; opacity: 0.22499999403953552; "></div>
        # self.driver.find_element_by_id('id_withdrawl_dialog').send_keys(Keys.ESCAPE) #Just hit Escape instead
        #In theaory, this should work, too: self.driver.find_element_by_id("cboxClose").click()

        
        #OK - now let'
        self.driver.find_element_by_partial_link_text('Cancel my enrollment').click()
        time.sleep(.5)
        self.driver.find_element_by_id("btn_withdraw_agree").click()
        eq_("Your Intranet > Transit Subsidy Withdrawl Confirmation", self.driver.title)


