from django.utils.unittest.case import skipIf
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from transit_subsidy.models import TransitSubsidy,Mode,OfficeLocation
import StringIO
import csv
import json as simplejson


class TransportationSubsidyViewTest(TestCase):
    fixtures = ['offices.json','transit_modes.json', 'users.json']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self):
        """
        Assumes valid user
        """
        self.user = User.objects.get(username='ted')
        is_logged_in = self.client.login(username='ted',password='ted')
        self.assertTrue(is_logged_in, 'Client not able to login?! Check fixture data or User creation method in setUp.')      
        self.office = OfficeLocation.objects.order_by('city')[0]
        

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


    def test_that_get_request_fails_must_be_a_POST(self):
        expected = 'error: please use POST'
        response = self.client.get('/transit/modes')
        print response
        self.assertEquals( expected, response.content )


        

