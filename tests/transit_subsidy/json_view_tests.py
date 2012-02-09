from django.utils.unittest.case import skipIf
from datetime import datetime
from django.test import TestCase
from front.models import OfficeLocation
from django.contrib.auth.models import User
from transit_subsidy.models import TransitSubsidy,Mode
import StringIO
import csv
from front.models import App,Person
import json as simplejson


class TransportationSubsidyViewTest(TestCase):
    fixtures = ['offices.json','transit_modes.json']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self):
        """
        Assumes valid user
        """
        self.user = User.objects.create_user('test_user','test_user@cfpb.gov','password')
        is_logged_in = self.client.login(username='test_user',password='password')
        #guard
        self.assertTrue(is_logged_in, 'Client not able to login?! Check fixture data or User creation method in setUp.')
              
        self.office = OfficeLocation.objects.order_by('city')[0]
        self.person = Person(user=self.user)
        self.person.first_name = 'Ted'
        self.person.last_name = 'Nugent'
        self.person.save()


    def tearDown(self):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def test_simple_json_fetch(self):
        
        response = self.client.post('/transit/modes')
        self.assertEquals(200, response.status_code)
        json_obj = simplejson.loads( response.content )
        self.assertTrue( len(json_obj) > 1 )
        self.assertEquals('AMTRAK', json_obj[0]['short_name'] )
        self.assertEquals('MARTZ', json_obj[12]['short_name'] )
        print json_obj[0]

        

