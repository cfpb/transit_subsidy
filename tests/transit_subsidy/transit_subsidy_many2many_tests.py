from django.utils.unittest.case import skipIf
from django.db.models import Avg, Max, Min, Count, Sum
from decimal import *
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from transit_subsidy.models import TransitSubsidy,TransitSubsidyForm,Mode,TransitSubsidyModes,OfficeLocation


class TransportationSubsidyMany2ManyTest(TestCase):
    fixtures = ['offices.json','transit_modes.json','users.json']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self):
        """
        Assumes valid user
        """
        self.user = User.objects.get(username='patti')
        is_logged_in = self.client.login(username='patti',password='patti')
        self.assertTrue(is_logged_in, 'Client not able to login?! Check fixture data or User creation method in setUp.')      
        self.office = OfficeLocation.objects.order_by('city')[0]        
        self.modes = Mode.objects.all()


    def tearDown(self):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# End-to-end test: create transit, save, create modes, save, assert
    def test_get_modes_as_string(self):
        trans = self._set_transit_subsidy()
        trans.save()

        # print self.modes
        #Metro
        _modes = TransitSubsidyModes(transit_subsidy=trans, mode=self.modes[0], cost=100)
        _modes.save()
        
        #Dash
        _modes = TransitSubsidyModes(transit_subsidy=trans, mode=self.modes[1], cost=50)
        _modes.save()

        #Other
        _modes = TransitSubsidyModes(transit_subsidy=trans, mode=self.modes[4], cost=5, other_mode='ScooterBus')
        _modes.save()

        self.assertTrue( self.modes[0].__unicode__() != None ) 
        self.assertTrue( _modes.__unicode__() != None )
    
    # End-to-end test: create transit, save, create modes, save, assert
    def test_create_simple_transit_subsidy(self):
        trans = self._set_transit_subsidy()
        trans.save()

        # print self.modes
        #Metro
        _modes = TransitSubsidyModes(transit_subsidy=trans, mode=self.modes[0], cost=100)
        _modes.save()
        
        #Dash
        _modes = TransitSubsidyModes(transit_subsidy=trans, mode=self.modes[1], cost=50)
        _modes.save()

        #Other
        _modes = TransitSubsidyModes(transit_subsidy=trans, mode=self.modes[4], cost=5, other_mode='ScooterBus')
        _modes.save()

        #Guard
        self.assertTrue( _modes.timestamp != None)
        
            
        ts_modes = TransitSubsidyModes.objects.all()
        actual = ts_modes.aggregate( Sum('cost') )
        print actual['cost__sum']
        
        self.assertEquals( Decimal('155.00'),  actual['cost__sum'] )

        trans2 = TransitSubsidy.objects.filter(user=self.user)[0]
        self.assertEquals('patti smith', trans2.signature)

        


    def _set_transit_subsidy(self):
        transit = TransitSubsidy()
        office = OfficeLocation.objects.order_by('city')[0]

        transit.user = self.user
        transit.destination = office
        transit.date_enrolled = '2011-06-23'
        transit.signature = 'patti smith'

        transit.origin_street = '123 Main Street'
        transit.origin_city = 'Anytown'
        transit.origin_state = 'VA'
        transit.origin_zip = '22222'
       
        
        transit.number_of_workdays = 20
        transit.daily_roundtrip_cost = 8
        transit.daily_parking_cost = 4
        transit.amount = 8
        transit.total_commute_cost = 160
        transit.dc_wmta_smartrip_id = '123-123-123'
        return transit
        # transit.save()
    