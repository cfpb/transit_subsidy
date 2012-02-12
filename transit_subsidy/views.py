import csv
from django.http import HttpResponse
from django import forms
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template import Template, Context
from django.contrib.auth.decorators import login_required
from dynamicresponse.response import *
from models import TransitSubsidy,TransitSubsidyForm,Mode,TransitSubsidyModes
from datetime import datetime
import json as simplejson
from django.views.decorators.csrf import csrf_exempt


SENDER = 'transitsubsidy@yourcompany.com'


@csrf_exempt
def modes_json(request):
    """
    Given a simple POST request, returns a JSON representation
    of all the available transportion modes.
    """
    if (request.method != 'POST'):
        return HttpResponse('error: please use POST')
    else:
        modes = Mode.objects.all()
        return JsonResponse(modes)



#util: should be here or ... ?
def get_segments(request):
    """ 
    Parses a querystring looking for parameters starting with 'segment-type',
    and returns a list of Dictionary objects representing commuting segements.
    These are intended to be persisted in a many-2-many intermediate relationship.

    *All* of the following are expected: segment-type_N, segement-amount_N, and, segments_N.
    """
    segments = []
    for name in request.POST:
        if name.startswith('segment-type'):
            segment_data = {}
            name_key = request.POST[name]
            if name_key == '' or name_key == None: continue
            cost_key = name.replace('type', 'amount')
            other = name.replace('type','other')
            other_key = request.POST[other]
        
            segment_data['type_id'] = request.POST[name]
            segment_data['amount'] = request.POST[cost_key]
            segment_data['other'] = other_key
    
            segments.append(segment_data)
    
    return  segments


@login_required
def home(request):
    """
    The main view -- landing page, form, and submission.  Upon submission
    the user should be redirected to a confirmation page and sent an email notification.
    """
    user = request.user

    if request.method == 'POST':
        form = TransitSubsidyForm(request.POST)
        # raise forms.ValidationError ('Intentional forms validation error.')

        if not form.is_valid():
            return render_to_response('transit_subsidy/index.html', {'form' : form, 'errors' : form.errors,
                                                                     'user' : request.user}, RequestContext(request))
        else:
            # Since the User object is in the request context on and not part of the form data,
            # we need to suspend the commit and create a new TransitSubsidy Object and add the user
            # to that instance prior to saving
            frm = form.save(commit=False)
            try:
                frm.date_enrolled = TransitSubsidy.objects.get(user=request.user).date_enrolled
            except TransitSubsidy.DoesNotExist:
                pass

            if None == frm.date_enrolled:
                frm.date_enrolled = datetime.now()

            frm.user = request.user
            frm.date_withdrawn =  None

            frm.save()

            #refactor!
            #Clear out existing. 
            TransitSubsidyModes.objects.filter(transit_subsidy=frm).delete()
            segments = get_segments(request)
            for segment in segments :
                _mode = Mode.objects.get( id=segment['type_id'] )
                _seg = TransitSubsidyModes(transit_subsidy=frm, mode=_mode, cost=segment['amount'], other_mode=segment['other'])
                _seg.save()
             
            modes = TransitSubsidyModes.objects.filter(transit_subsidy=frm)    

            send_notification(request.user,frm) #user and transit objects as args

            return render_to_response('transit_subsidy/thank_you.html', {'form' : frm, 'user' : request.user, 'modes': modes,
                                                                     'success_message': 'OK!'}, RequestContext(request))
    else:
        try:
            transit = TransitSubsidy.objects.get(user=request.user)
            # Because of ATO, we shouldn't need to encrypt this, but we could if needed:
            # transit.last_four_ssn = decrypt(__KEY,transit.last_four_ssn)
            returning_user = True
            timestamp = transit.timestamp
            modes = TransitSubsidyModes.objects.filter(transit_subsidy=transit)
        except TransitSubsidy.DoesNotExist:
            transit = TransitSubsidy()
            returning_user = False
            timestamp = None
            modes = None
        form = TransitSubsidyForm(instance=transit)
        return render_to_response('transit_subsidy/index.html', {'form' : form, 'user' : request.user,
                                                                 'returning_user': returning_user,
                                                                 'modes': modes, 'timestamp' : timestamp,
                                                                 'transit': transit },
                                                                  RequestContext(request) )



def send_notification(user, transit):
    """
    Sends an email notification to the person who submitted the transit subsidy request.
    
    @param user:  the person who requested the subsidy
    @param transit: L{TransitSubsidy} the transit subsidy claim object
    """
    _sender = SENDER
    _subject = 'Transit Subsidy Program: Thank You for Beginning Your Enrollment'
    message = Template("""
    <style>html,p{font-family: arial, helvetica}</style>

    <p>Dear {{user.first_name}},</p>

    <p>Thank you for your enrollment in the CFPB TransitSubsidy Program!</p>

    <p>You submitted a Transit Subsidy request on {{ transit.timestamp }} for ${{ transit.amount }} per month.</p>

    """)

    ctx = Context({'user':user,'transit':transit})

    # send_mail('Transit Subsidy Request Confirmation', message.render(ctx), sender, [user.email])
    
    subject, from_email, to = _subject, _sender, user.email
    text_content = message.render(ctx)
    html_content = message.render(ctx)
    e = EmailMultiAlternatives(subject, html_content, from_email, [to])
    e.attach_alternative(html_content, "text/html")
    e.content_subtype = "html"
    e.send()



@login_required
def cancel(request):
    if (request.method != 'POST'):
        raise Exception('Please POST to this URL')
    else:
        transit = TransitSubsidy.objects.get(user=request.user)
        transit.date_withdrawn = datetime.now()
        transit.save()
        return render_to_response('transit_subsidy/cancel.html', { 'user' : request.user, 'transit': transit},
                                                                    RequestContext(request) )
        



#Lots to do here!
@login_required
def dump_csv(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=transit_subsidy.csv'
    claims = TransitSubsidy.objects.all()
    writer = csv.writer(response)
    writer.writerow([   'Last Name', 'First Name', 'Email','Last Four SSN',  
                        'Date Enrolled', 'Date Updated', 'Origin Location', 'Destination', 
                        'Number of Workdays', 'Daily Roundtrip Cost',
                        'Daily Parking Cost', 'Total Claim Amount', 'DC Metro Smartrip No.'])
    for claim in claims:
        user = claim.user 
        writer.writerow([
                          user.last_name.encode('ascii','ignore'), 
                          user.first_name.encode('ascii','ignore'),
                          user.email.encode('ascii','ignore'),
                          claim.last_four_ssn,
                          claim.date_enrolled,
                          claim.timestamp, 
                          claim.origin_street + ' ' + claim.origin_city.encode('ascii','ignore') + ' ' + 
                          claim.origin_state + ' ' +  claim.origin_zip,
                          # claim.route_description.encode('ascii','ignore'),
                          claim.destination,
                          claim.number_of_workdays,
                          claim.daily_roundtrip_cost,
                          claim.daily_parking_cost,
                          claim.amount,
                          claim.dc_wmta_smartrip_id,
                          # claim.terms_of_service,
                          # claim.supervisor_approval,                        
                        ])

    return response



