from base_test import *

#---------------------- Fixture ----------------------#


def setup_module(module):
    global driver 
    logger.info('setup_module: %s' % module.__name__)
    driver = new_driver()

def teardown_module(module):
    global driver
    logger.info('teardown_module %s' % module.__name__)
    driver.quit()

#------------------------------------------------------#

base_url = "http://localhost:8000"


def first():
    driver.get(base_url + "/login")

def last():
    driver.get(base_url + "/logout")
    # driver.find_element_by_link_text('Reset Form').click()


#Patti Smith registers Or Updates
@with_setup(first,last)
def test_end2end_PattiSmith_OnTheBus():
    driver.get(base_url + "/login/")
    eq_("Your Intranet >", driver.title)

    driver.find_element_by_id("id_username").clear()
    driver.find_element_by_id("id_username").send_keys("patti")
    driver.find_element_by_id("id_password").clear()
    driver.find_element_by_id("id_password").send_keys("patti")
    driver.find_element_by_id("btn_login").click()
    eq_("Your Intranet > Transit Subsidy Request", driver.title)

    driver.find_element_by_id("id_origin_street").clear()
    driver.find_element_by_id("id_origin_street").send_keys("123 Main St")
    driver.find_element_by_id("id_origin_city").clear()
    driver.find_element_by_id("id_origin_city").send_keys("Anytown")
    driver.find_element_by_id("id_origin_state").clear()
    driver.find_element_by_id("id_origin_state").send_keys("VA")
    driver.find_element_by_id("id_origin_zip").clear()
    driver.find_element_by_id("id_origin_zip").send_keys("12345")
    driver.find_element_by_id("id_destination").find_elements_by_tag_name('option')[5].click() #1700 G
    try:
        driver.find_element_by_id("segment-type_1").find_elements_by_tag_name('option')[2].click()
        driver.find_element_by_id("segment-amount_1").clear()
        driver.find_element_by_id("segment-amount_1").send_keys("1.5")
        driver.find_element_by_id("add_1").click()
        driver.find_element_by_id("segment-type_2").find_elements_by_tag_name('option')[15].click()
        driver.find_element_by_id("segment-amount_2").clear()
        driver.find_element_by_id("segment-amount_2").send_keys("2.25")
    except NoSuchElementException as e:  #returning user workaround
        driver.find_element_by_id("segment-type_2").find_elements_by_tag_name('option')[2].click()
        driver.find_element_by_id("segment-amount_2").clear()
        driver.find_element_by_id("segment-amount_2").send_keys("1.5")
        driver.find_element_by_id("segment-type_3").find_elements_by_tag_name('option')[15].click()
        driver.find_element_by_id("segment-amount_3").clear()
        driver.find_element_by_id("segment-amount_3").send_keys("2.25")



    driver.find_element_by_xpath("(//input[@id='id_work_sked'])[2]").click()
    driver.find_element_by_id("id_help_smartrip").click()
    zzz()
    driver.find_element_by_id("cboxClose").click()
    zzz()
    # driver.find_element_by_css_selector("span.form_elem > span.form_elem > label.infield").click()
    driver.find_element_by_id("id_dc_wmta_smartrip_id").clear()
    driver.find_element_by_id("id_dc_wmta_smartrip_id").send_keys("123-123-123")
    driver.find_element_by_id("btn_enroll_smartrip").click()
    zzz()
    driver.find_element_by_id("id_last_four_ssn").send_keys("1111")
    driver.find_element_by_id("id_signature").send_keys("Patti Smith")
    driver.find_element_by_id("btn_agree").click()
    eq_("Your Intranet > Transit Subsidy Confirmation", driver.title)




#Ted (who does not have a claim) tries to register without entering any fields   
@with_setup(first,last)
def test_form_validation():
    driver.find_element_by_id("id_username").clear()
    driver.find_element_by_id("id_username").send_keys("ted")
    driver.find_element_by_id("id_password").clear()
    driver.find_element_by_id("id_password").send_keys("ted")
    driver.find_element_by_id("btn_login").click()
    eq_("Your Intranet > Transit Subsidy Request", driver.title)


    driver.get(base_url + '/transit')
    driver.find_element_by_id('btn_enroll_smartrip').click()
    
    messages = ['You must select your office location',
                'Select a segment and enter an amount.',
                'Please select one work schedule option',
                'Select at least one work schedule option above',
                'Specify commuting segments, costs, and work schedule', 
                'We need your home address (Street, City, State, Zip)']
    
    for m in messages:
        yield valididate_messages , driver, m
    
 
def valididate_messages(driver,message):
    is_textpresent(driver, message)
   



@with_setup(first,last)
def test_end2end_TedNugent_Cancels_at_last_minute():
    driver.get(base_url + "/login/")
    eq_("Your Intranet >", driver.title)

    driver.find_element_by_id("id_username").clear()
    driver.find_element_by_id("id_username").send_keys("ted")
    driver.find_element_by_id("id_password").clear()
    driver.find_element_by_id("id_password").send_keys("ted")
    driver.find_element_by_id("btn_login").click()
    eq_("Your Intranet > Transit Subsidy Request", driver.title)

    driver.find_element_by_id("id_origin_street").clear()
    driver.find_element_by_id("id_origin_street").send_keys("123 Sunset Ave")
    driver.find_element_by_id("id_origin_city").clear()
    driver.find_element_by_id("id_origin_city").send_keys("Holywood")
    driver.find_element_by_id("id_origin_state").clear()
    driver.find_element_by_id("id_origin_state").send_keys("CA")
    driver.find_element_by_id("id_origin_zip").clear()
    driver.find_element_by_id("id_origin_zip").send_keys("90027")
    driver.find_element_by_id("id_destination").find_elements_by_tag_name('option')[7].click() 

    driver.find_element_by_id("segment-type_1").find_elements_by_tag_name('option')[17].click()
    driver.find_element_by_id("segment-other_1").send_keys('Limo')
    driver.find_element_by_id("segment-amount_1").clear()
    driver.find_element_by_id("segment-amount_1").send_keys("400")

    driver.find_element_by_xpath("(//input[@id='id_work_sked'])[4]").click()
    driver.find_element_by_id('id_number_of_workdays').clear()
    driver.find_element_by_id('id_number_of_workdays').send_keys('1')
    driver.find_element_by_id('id_total_commute_cost').click() #fire js validation event
    driver.find_element_by_id("btn_enroll_smartrip").click()
    zzz()
    driver.find_element_by_id("btn_no_agree").click()
    eq_("Your Intranet > Transit Subsidy Request", driver.title)
    


#Bug with element.text?
# @with_setup(first,last)
def _add_segments():
    sel1 = driver.find_element_by_id('segment-type_1')
    options1 = sel1.find_elements_by_tag_name('option')
    options1[1].click()
    driver.find_element_by_id('segment-amount_1').send_keys('4.25')
    driver.find_element_by_id('add_1').click()

    sel1 = driver.find_element_by_id('segment-type_2')
    options1 = sel1.find_elements_by_tag_name('option')
    options1[1].click()
    driver.find_element_by_id('segment-amount_2').send_keys('1.75')
    driver.find_element_by_id('add_2').click()
    zzz()
    e = driver.find_element_by_id('segment-amount_1')
    logger.info( e.text )

    street = driver.find_element_by_id('id_origin_street')
    street.send_keys('123 Main St.')
    logger.info( street.text )
    logger.info( street.tag_name )
    # driver.find_element_by_id('remove_3').click()
    total = driver.find_element_by_id('totals').text
    # eq_(6, total)








