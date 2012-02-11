from base_test import *

#---------------------- Fixture ----------------------#

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
    pass

def last():
    driver.get(base_url + "/logout")



#Ted (who does not have a claim) tries to register without entering any fields   
@with_setup(first,last)
def test_form_validation():
    transit.login('ted','ted')

    driver.get(base_url + '/transit')
    driver.find_element_by_id('btn_enroll_smartrip').click()
    
    messages = ['You must select your office location',
                'Select a segment and enter an amount.',
                'Please select one work schedule option',
                'Select at least one work schedule option above',
                'Specify commuting segments, costs, and work schedule', 
                'We need your home address (Street, City, State, Zip)']
    
    def valididate_messages(message):
        is_textpresent(driver, message)
   
    for m in messages:
        yield valididate_messages , m
    



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
    # driver.find_element_by_id('id_total_commute_cost').click() #fire js validation event
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
def test_iterate_all_segments():
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







    # transit.commute_from("123 Sunset Ave", "Hollywood", "CA", "90029")
    # transit.commute_to(7)    
    
