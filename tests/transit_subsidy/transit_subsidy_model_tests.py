from django.utils.unittest.case import skipIf
from datetime import datetime
from django.test import TestCase
from front.models import OfficeLocation
from django.contrib.auth.models import User
from transit_subsidy.models import TransitSubsidy,TransitSubsidyForm
from front.models import Person


class TransportationSubsidyModelTest(TestCase):
    fixtures = ['offices.json']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self):
        """
        Assumes valid user
        """
        self.user = User.objects.create_user('test_user','test_user@cfpb.gov','password')
        is_logged_in = self.client.login(username='test_user',password='password')
        self.assertTrue(is_logged_in, 'Client not able to login?! Check fixture data or User creation method in setUp.')
        self.office = OfficeLocation.objects.order_by('city')[0]


    def tearDown(self):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # --- To Do: Refactor to model_form_tests

    def test_wrong_days_at_work_should_cause_form_error(self):
        data = self._get_good_post_data()
        data['number_of_workdays'] = 50
        t_form = TransitSubsidyForm( data  )
        self.assertFalse( t_form.is_valid() , "Should be a bad form for WORK DAYS")
        data['number_of_workdays'] = -1
        t_form = TransitSubsidyForm( data  )
        self.assertFalse( t_form.is_valid() , "Should be a bad form for WORK DAYS")


    def test_wrong_amount_at_work_should_cause_form_error(self):
        data = self._get_good_post_data()
        data['amount'] = 500
        t_form = TransitSubsidyForm( data  )
        self.assertFalse( t_form.is_valid() , "Should be a bad form for AMOUNT")
        data['amount'] = -1
        t_form = TransitSubsidyForm( data  )
        self.assertFalse( t_form.is_valid() , "Should be a bad form for AMOUNT")    



    def test_bad_ssn_should_cause_form_error(self):
        data = self._get_good_post_data()
        data['last_four_ssn'] = '*bZ'
        t_form = TransitSubsidyForm( data  )
        self.assertFalse( t_form.is_valid() , "Should be a bad form SSN.")


    def test_unicode_should_return_test_user(self):
        self._set_transit_subsidy()
        trans = TransitSubsidy.objects.filter(user=self.user)[0]
        actual =  unicode(trans).find('test_user')
        self.assertTrue( actual > 0 )


    def test_basic_transit_subsidy_model_creation(self):
        """
        Test basic transit subsidy model creation

        """
        self._set_transit_subsidy()
        actual = TransitSubsidy.objects.filter(user=self.user)
        self.assertEquals( self.user, actual[0].user, "Different users" )
    


    def test_unicode_to_string(self):        
        """
        Test unicode to string.
        """
        expected = 'test_user'
        self._set_transit_subsidy()
        ts = TransitSubsidy.objects.filter(user=self.user)
        actual =  unicode(ts[0].user)
        self.assertEquals( expected, actual, "Why this thing went horribly wrong." )
    
    


     #Util method
    def _get_good_post_data(self):
        return {  'date_enrolled' : datetime.now(),
                  'timestamp' : datetime.now(),
                  'last_four_ssn': '1111',
                  'origin_street': '123 Main St.',
                  'origin_city':'Anytown',
                  'origin_state':'OO',
                  'origin_zip':'12345',
                  'route_description': 'from here to there',
                  'destination': self.office.id,
                  'number_of_workdays': 20,
                  'daily_roundtrip_cost' : 8,
                  'daily_parking_cost': 4,
                  'amount': 164,
                  'terms_of_service' : True,
                  'supervisor_approval': True}



    def _set_transit_subsidy(self):
        transit = TransitSubsidy()
        office = OfficeLocation.objects.order_by('city')[0]

        transit.user = self.user
        transit.signature = 'foo'
        transit.destination = office
        transit.date_enrolled = '2011-06-23'

        transit.origin_street = '123 Main Street'
        transit.origin_city = 'Anytown'
        transit.origin_state = 'VA'
        transit.origin_zip = '22222'
        transit.route_description = "Harbor bus to City Subway stop to Work Subway"
        
        transit.number_of_workdays = 20
        transit.daily_roundtrip_cost = 8
        transit.daily_parking_cost = 4
        transit.amount = 8
        transit.total_commute_cost = 160
        transit.dc_wmta_smartrip_id = '123-123-123'
        
        transit.save()
    