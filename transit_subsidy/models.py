__author__ = 'CFPB Labs'
__version__ = '0.9.1'
#-------------------------------------------------------------------------------
from django.db import models
from django.forms.widgets import Select,HiddenInput,Textarea
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
import re


MAX_CLAIM = 125


class OfficeLocation (models.Model):
    """
    Represents a CFPB office.  Details with respect to room number or
    office number, floor, etc., are intentionally omitted

    @author: CFPB Labs
    @date: 09/28/2011
    @contact: bill
    """
    id = models.CharField(max_length=12,primary_key=True)
    street = models.CharField(max_length=56)
    suite = models.CharField(max_length=56, blank=True, null=True)
    city = models.CharField(max_length=56)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)

    def __unicode__(self):
        return '%s, %s, %s %s' % (self.street, self.city, self.state, self.zip)


class Mode(models.Model):
    """Represents a transit subsidy benefit abstraction for a mode of transportation.

    @organization: CFPB Labs
    @date:  11/18/2011
    @author: miklane

    """
    class Meta:
        ordering = ["short_name"]
        
    long_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=56)
    url_link = models.CharField(max_length=1000, null=True, blank=True)
    """Example:Smartrip,Debit Card,Metro Check"""
    distribution_method = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)


    def __unicode__(self):
        return u'%s, %s, %s, %s' % (self.long_name, self.short_name, self.locality, self.distribution_method)



class TransitSubsidyModes(models.Model):
    # manager = models.Manager() #renaming as 'objects' seems idiomatic to querying
    transit_subsidy = models.ForeignKey('TransitSubsidy')
    mode = models.ForeignKey('Mode')
    cost = models.DecimalField(decimal_places=2,max_digits=5) 
    other_mode = models.CharField(max_length=64, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return u'%s, %s, %s, %s' % (self.transit_subsidy, self.mode, self.cost, self.timestamp)




class TransitSubsidy(models.Model):
    """
    Represents a transit subsidy benefit abstraction for an individual/employee.

    @organization: CFPB Labs
    @date:  09/28/2011
    @author: bill
    
    """

    modes = models.ManyToManyField(Mode, through='TransitSubsidyModes')

    user = models.ForeignKey(User,primary_key=True)

    destination = models.ForeignKey( OfficeLocation )

    #one time only! If not exists assume new. Do once.
    date_enrolled = models.DateTimeField()
    date_withdrawn = models.DateTimeField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    last_four_ssn = models.CharField(max_length=56)
    signature = models.CharField(max_length=56)

    origin_street = models.CharField(max_length=56)
    origin_city = models.CharField(max_length=56)
    origin_state = models.CharField(max_length=2)
    origin_zip = models.CharField(max_length=5)
    
    
    number_of_workdays = models.SmallIntegerField() #Choice: 20,16,# 18, or other
    daily_roundtrip_cost = models.DecimalField(decimal_places=2,max_digits=5)
    daily_parking_cost = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    
    total_commute_cost = models.DecimalField(decimal_places=2,max_digits=5)
    """ The amount being distributed """ 
    amount = models.DecimalField(decimal_places=2,max_digits=5)
    dc_wmta_smartrip_id = models.CharField( max_length=56, blank=True, null=True)

    approved_on = models.DateTimeField(null=True,blank=True)
    approved_by = models.CharField(max_length=56,null=True,blank=True)

    def __unicode__(self):
        return u'%s %s <%s>' % (self.user.last_name, self.user.first_name, self.user.username)




        
class  TransitSubsidyForm(ModelForm):
    """
        A ModelForm based on the TransitSubsidy model
        
        @author: CFPB Labs
    """

    
    def clean(self):
        data = self.cleaned_data
        #print data
        return data
    
    def clean_last_four_ssn(self):
        """The last four of an SSN (not encrypted)"""
        ssn = self.cleaned_data['last_four_ssn']
        pattern = re.compile('[0-9]{4}')
        if ( pattern.match(ssn) == None ):
            raise forms.ValidationError ('This must be exactly four digits.')
        # return encrypt(_KEY,ssn)
        return ssn

    def clean_number_of_workdays(self):
        """Constraint 1-31 days"""
        days = self.cleaned_data['number_of_workdays']
        if days > 31:
            raise forms.ValidationError ('You can''t work more than 31 days in a month.')
        if days < 1:
            raise forms.ValidationError ('Looks like you entered 0 less for the days per month you work. Really?')
        return days

    def clean_amount(self):
        """ $125 max"""
        amt = self.cleaned_data['amount']
        if amt > MAX_CLAIM:
            raise forms.ValidationError('The most you can request is $%s.' % MAX_CLAIM )
        if amt < 1:
            raise forms.ValidationError('Really?! That looks to be 0 or less.')
        return amt

    
    class Meta:
        model = TransitSubsidy
        #'person_name', 
        fields = ( 'last_four_ssn', 'origin_street', 'origin_city', 'origin_state', 'origin_zip',
                   'destination', 'number_of_workdays', 'dc_wmta_smartrip_id',
                   'amount', 'total_commute_cost', 'daily_parking_cost', 'daily_roundtrip_cost', 'signature' )

        widgets = {
            'id': HiddenInput(),
            'route_description': Textarea(attrs={'rows': 2, 'cols': 53,}),
        }

        

  
