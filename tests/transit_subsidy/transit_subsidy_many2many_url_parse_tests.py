"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.http import QueryDict
from transit_subsidy.views import *
from transit_subsidy.models import Mode,TransitSubsidy,TransitSubsidyModes

class TransitModelTests(TestCase):

    fixtures = ['transit_modex.json']
    




class TransitViewTests(TestCase):


    #TechDebt: Does the ordering matter?    
    def test_that_segments_are_parsed(self):
        request = QueryDict('')
        query_string  = 'segment-type_0=1&segment-amount_0=1&segment-other_0=&'
        query_string += 'segment-type_1=2&segment-amount_1=3&segment-other_1=&'
        query_string += 'segment-type_2=3&segment-amount_2=5&segment-other_2=&'
        query_string += 'segment-type_3=4&segment-amount_3=7&segment-other_3=&'
        
        request.POST = QueryDict(query_string)
        actual = get_segments(request)
        # print actual;
        seg_1 = actual[0]
        seg_2 = actual[1]
        seg_3 = actual[2]
        seg_4 = actual[3]

        # print '\n'
        # print '-----------------------------'
        # print seg_1;
        # print '-----------------------------'
        # print seg_2;
        # print '-----------------------------'
        # print seg_3;
        # print '-----------------------------'
        # print seg_4;
        # print 

        self.assertEqual( u'3', seg_1['type_id'])
        self.assertEqual( u'5', seg_1['amount'])

        self.assertEqual( u'4', seg_2['type_id'])
        self.assertEqual( u'7', seg_2['amount'])

        self.assertEqual( u'2', seg_3['type_id'])
        self.assertEqual( u'3', seg_3['amount'])

        self.assertEqual( u'1', seg_4['type_id'])
        self.assertEqual( u'1', seg_4['amount'])



    #This test is hard to read, but it's correct
    def test_that_segments_are_parsed_out_of_order(self):
        request = QueryDict('')
        query_string  = 'segment-type_0=2&segment-amount_0=1&segment-other_0=&'
        query_string += 'segment-type_1=4&segment-amount_1=3&segment-other_1=&'
        query_string += 'segment-type_2=1&segment-amount_2=5&segment-other_2=&'
        query_string += 'segment-type_3=3&segment-amount_3=7&segment-other_3=&'
        
        request.POST = QueryDict(query_string)
        actual = get_segments(request)
        # print actual;
        seg_1 = actual[0]
        seg_2 = actual[1]
        seg_3 = actual[2]
        seg_4 = actual[3]

        # print '\n'
        # print '-----------------------------'
        # print seg_1;
        # print '-----------------------------'
        # print seg_2;
        # print '-----------------------------'
        # print seg_3;
        # print '-----------------------------'
        # print seg_4;
        # print 

        self.assertEqual( u'1', seg_1['type_id'])
        self.assertEqual( u'5', seg_1['amount'])

        self.assertEqual( u'3', seg_2['type_id'])
        self.assertEqual( u'7', seg_2['amount'])

        self.assertEqual( u'4', seg_3['type_id'])
        self.assertEqual( u'3', seg_3['amount'])

        self.assertEqual( u'2', seg_4['type_id'])
        self.assertEqual( u'1', seg_4['amount'])

   #This test is hard to read, but it's correct
    def test_that_other_segments_are_parsed(self):
        request = QueryDict('')
        query_string  = 'segment-type_0=-1&segment-amount_0=1&segment-other_0=The%20Local%20Bus&'
        query_string += 'segment-type_3=3&segment-amount_3=7&segment-other_3=&'
        request.POST = QueryDict(query_string)
        actual = get_segments(request)
        # print actual;
        seg_1 = actual[0]
        seg_2 = actual[1]

        self.assertEqual( u'-1', seg_1['type_id'])
        self.assertEqual( u'1', seg_1['amount'])
        self.assertEqual( u'The Local Bus', seg_1['other'])

        self.assertEqual( u'3', seg_2['type_id'])
        self.assertEqual( u'7', seg_2['amount'])
        self.assertEqual( u'', seg_2['other'])


    def test_that_disparate_segments_are_ignored(self):
        request = QueryDict('')
        query_string = 'foo=bar&asd=asd&segment-type_0=metro&segment-amount_0=180&x=z&segment-other_0='
        request.POST = QueryDict(query_string)
        actual = get_segments(request)
        # self.assertEqual( u'180', actual['metro'])
        print actual
