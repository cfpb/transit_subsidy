__author__ = "CFPBLabs"

""" 
 Tests the TransitSubsidyApp which abstract the functionality of the actual application.
"""


from base_test import *

#---------------------- Fixture ----------------------#


# Assumes tests will be run on the same server the app is running on.
# Obviously, this will have to be changed if testing a remote instance.
base_url = "http://localhost:8000"  



def setup_module(module):
    global driver , transit , base_url
    logger.info('setup_module: %s' % module.__name__)
    driver = new_driver()
    transit = TransitSubsidyApp(driver,base_url)


def teardown_module(module):
    global driver
    logger.info('teardown_module %s' % module.__name__)
    driver.quit()

#------------------------------------------------------#


def first():
    time.sleep(1)

def last():
    driver.get(base_url + "/logout")



@with_setup(first,last)
def test_that_patti_smith_withdraws_enrollment():
    transit.login('patti','patti')
    transit.withdraw_enrollment()


#Ted (who does not have a claim) tries to register without entering any fields   
@with_setup(first,last)
def test_form_validation():
    transit.login('ted','ted')

    driver.get(base_url + '/transit')
    driver.find_element_by_id('btn_enroll_smartrip').click()
    
    ids = [ 'id_origin_zip', 'segment-amount_1', 'work_sked', 'id_number_of_workdays', 'id_amount']

    def valididate_messages(id):
        e = driver.find_element_by_css_selector('em[for="%s"]' % id)
        expected = 'error'  # Will be "success" when validation passes
        actual = e.get_attribute('class')
        eq_( expected, actual, "Validation error should be present for : %s" % id)   
    
    for id in ids:
        yield valididate_messages , id
    


#Patti Smith registers Or Updates
@with_setup(first,last)
def test_end2end_PattiSmith_OnTheBus():
    
    transit.login('patti','patti')
    transit.commute_from()
    transit.commute_to()
    
    try:
        transit.add_segment( segment_id='1', mode_id=2, amount='1.5', add_another=True )
        transit.add_segment( segment_id='2', mode_id=15, amount='2.25', add_another=False )
    
    #If returning user, the first empty segment (id=1) is removed
    except NoSuchElementException as e: 
        transit.add_segment( segment_id='2', mode_id=2, amount='1.50', add_another=False )
        transit.add_segment( segment_id='3', mode_id=15, amount='2.25', add_another=False )

    transit.select_workdays(1)
    transit.view_smartriphelp()
    zzz()
    transit.add_smartrip()
    transit.enroll()
    transit.sign('1234','Patti Smith')




@with_setup(first,last)
def test_end2end_TedNugent_Cancels_at_last_minute():    
    transit.login('ted','ted')
    transit.commute_from("123 Sunset Ave", "Hollywood", "CA", "90029")
    transit.commute_to(7)    
    transit.add_other_segment("1", "Limo", "400", False)
    transit.select_workdays(id=4, other='1')
    transit.enroll()
    transit.dont_sign()




@with_setup(first,last)
def test_add_2_segments_eq_6_bucks():
    transit.login('patti','patti')
    transit.add_segment( segment_id='2', mode_id=1, amount='4.25', add_another=False )
    transit.add_segment( segment_id='3', mode_id=5, amount='1.75', add_another=True )
    transit.remove_segment( segment_id='3')
    transit.add_segment( segment_id='4', mode_id=3, amount='1.75', add_another=False )
    _total = driver.find_element_by_id('totals').get_attribute('value')
    eq_( '6.00', _total)



@with_setup(first,last)
def test_validate_smartrip_segments():
    transit.login()
    # return
    sel = driver.find_element_by_id('segment-type_1')
    options = sel.find_elements_by_tag_name('option')
    

    def exercise_option(i):
        id = str(i)
        transit.add_segment( segment_id=id, mode_id=i, amount='1', add_another=True )
        
    for i in range(1,len(options)):
        # logger.info( 'i=%s' % i )
        yield exercise_option, i
    
    total = driver.find_element_by_id('totals').get_attribute('value')
    expected = len(options)-1
    eq_( str(expected) + '.00', total )




@with_setup(first,last)
def test_iterate_Smartrip_segments():
    transit.login()
    #Potentially brittle: IDs for Art,Dash,Metro Bus,Metro
    smartrips = [2,6,15,16]

    def exercise_option(id):
        transit.add_segment( segment_id='1', mode_id=id, amount='1', add_another=False )
        transit.enroll()
        is_textpresent(driver,'Enter your Smartip card number')
        
    for id in smartrips:
        transit.reset()
        yield exercise_option, id
    
    

@with_setup(first,last)
def test_Smartrip_length():
    transit.login()
    transit.add_segment( segment_id='1', mode_id=2, amount='1', add_another=False )
    transit.add_smartrip('12345678')
    transit.enroll()
    e = driver.find_element_by_css_selector('em[for="id_dc_wmta_smartrip_id"]')
    expected = 'error'
    actual = e.get_attribute('class')
    eq_( expected, actual, "Smartrip error should be present.")

    

@with_setup(first,last)
def test_add_remove_many_segments():    
    transit.login()
    transit.add_segment( segment_id='1', mode_id=1, amount='1', add_another=True )
    transit.add_segment( segment_id='2', mode_id=2, amount='2', add_another=True )
    transit.add_segment( segment_id='3', mode_id=3, amount='3', add_another=True )
    transit.add_segment( segment_id='4', mode_id=4, amount='4', add_another=False )

    transit.remove_segment(2)
    transit.click_add() #5
    transit.add_segment( segment_id='5', mode_id=5, amount='5', add_another=False )

    transit.remove_segment(4)
    transit.click_add() #6
    transit.add_segment( segment_id='6', mode_id=6, amount='6', add_another=False )

    transit.remove_segment(6)
    transit.remove_segment(5)
    transit.remove_segment(3)
    transit.reset()

