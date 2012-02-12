import time
from django.utils.unittest.case import skipIf
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from transit_subsidy.models import TransitSubsidy,TransitSubsidyForm,OfficeLocation
from django.contrib.auth.models import User

class TransportationSubsidyModelTest(TestCase):
    fixtures = ['offices.json','users.json'] 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self):
        """
        Assumes valid user
        """
        self.user = User.objects.get(username='jimi')
        is_logged_in = self.client.login(username='jimi',password='jimi')
        self.assertTrue(is_logged_in, 'Client not able to login?! Check fixture data or User creation method in setUp.')      
        self.office = OfficeLocation.objects.order_by('city')[0]


    def tearDown(self):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

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
        actual =  unicode(trans).find('jimi')
        self.assertTrue( actual > 0 )


    def test_basic_transit_subsidy_model_creation(self):
        self._set_transit_subsidy()
        actual = TransitSubsidy.objects.filter(user=self.user)
        self.assertEquals( self.user, actual[0].user, "Different users" )
    


    def test_unicode_to_string(self):        
        expected = 'jimi'
        self._set_transit_subsidy()
        ts = TransitSubsidy.objects.filter(user=self.user)
        actual =  unicode(ts[0].user)
        self.assertEquals( expected, actual, "Why this thing went horribly wrong." )
    
    
    def test_enroll_then_cancel(self):
        t = self._set_transit_subsidy()
        id = t.pk
        ts = TransitSubsidy.objects.get(pk=id)
        _now = datetime.now()
        time.sleep(.379987612123676871236) #try to throw a wrench in time
        ts.date_withdrawn = _now
        ts.save()
        ts2 = TransitSubsidy.objects.get(pk=id)
        self.assertEquals( ts2.date_withdrawn, _now, "These values should be the same" )
        self.assertEquals( ts2.date_withdrawn, ts.date_withdrawn, "These values should be the same" )



     #Util method
    def _get_good_post_data(self):
        return {  'date_enrolled' : datetime.now(),
                  'timestamp' : datetime.now(),
                  'data_withdrawn': None,
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
                  'amount': 125,
                  'terms_of_service' : True,
                  'supervisor_approval': True}



    def _set_transit_subsidy(self):
        transit = TransitSubsidy()
        office = OfficeLocation.objects.order_by('city')[0]

        transit.user = self.user
        transit.signature = 'foo'
        transit.destination = office
        transit.date_enrolled = '2011-06-23'
        transit.date_withdrawn = None

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
        return transit
    