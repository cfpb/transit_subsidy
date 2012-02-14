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

            send_enrollment_notification(request.user,frm) #user and transit objects as args

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



def send_enrollment_notification(user, transit):
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

    <p>Thank you for your enrollment in the Transit Subsidy Program!</p>

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


def send_withdrawl_notification(user):
    """
    Sends an email notification to the person who requested to be withdrawn from the program.
    
    @param user:  the person who requested the subsidy
    """
    _sender = SENDER
    _subject = 'Transit Subsidy Program: Thank You for Beginning Your Enrollment'
    message = Template("""
    <style>html,p{font-family: arial, helvetica}</style>

    <p>Dear {{user.first_name}},</p>

    <p>You have been withdrawn from the Transit Subsidy Program on {{ transit.timestamp }}.</p>

    <p>This will be reflected in the next cycle.  Also, if you need to re-enroll, please visit 
    the enrollment application again.
    </p>

    """)

    ctx = Context({'user':user})
    
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
        send_withdrawl_notification(request.user)
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




@login_required
def approval_json(request):
    # return HttpResponse('asdasd')
    # Distribution buckets, need to compute
    # TranBen , Smartrip, Regional, Other, TRANServe
    res = u''
    json = { 'page':0, 'total': 0 , 'records': 0, 'rows': [] }
    modes  = TransitSubsidyModes.objects.all()

    #res +=   unicode( Mode.objects.values('distribution_method') )
    res += '\n\n'
    
    for trans in TransitSubsidy.objects.all():
        _tran_info = {}
        
        ts_modes = TransitSubsidyModes.objects.filter( transit_subsidy=trans )
        _tran_info['id'] = unicode(trans.user_id)
        _tran_info['username'] = unicode(trans.user.username) 
        _tran_info['first_name'] = unicode(trans.user.first_name)
        _tran_info['last_name'] = unicode(trans.user.last_name)
        _tran_info['name'] = '%s, %s' % (unicode(trans.user.last_name),unicode(trans.user.first_name))
        _tran_info['email'] = unicode(trans.user.email)
        _tran_info['total_amount'] =  unicode(trans.amount)
        _tran_info['last_four_ssn'] =  unicode(trans.last_four_ssn)
        _tran_info['date_enrolled'] =  unicode(trans.date_enrolled)
        _tran_info['timestamp'] =  unicode(trans.timestamp) 
        _tran_info['origin_street'] =  unicode(trans.origin_street)
        _tran_info['origin_city'] =  unicode(trans.origin_city.encode('ascii','ignore') ) 
        _tran_info['origin_state'] =  unicode(trans.origin_state)
        _tran_info['origin_zip'] =  unicode(trans.origin_zip)
        _tran_info['origin_address'] = '%s %s, %s %s' % (_tran_info['origin_street'],_tran_info['origin_city'],_tran_info['origin_state'],_tran_info['origin_zip'])
        _tran_info['destination'] =  unicode(trans.destination)
        _tran_info['workdays'] =  unicode(trans.number_of_workdays)
        _tran_info['daily+roundtrip_cost'] =  unicode(trans.daily_roundtrip_cost)
        _tran_info['daily_parking_cost'] =  unicode(trans.daily_parking_cost)
        _tran_info['smartrip_id'] =  unicode(trans.dc_wmta_smartrip_id)
        _tran_info['approved_by'] =  unicode(trans.approved_by)
        _tran_info['approved_on'] =  unicode(trans.approved_on)
        _tran_info['modes'] = [ (mode) for mode in modes.filter(transit_subsidy=trans) ]
        json['rows'].append(_tran_info)        
    return JsonResponse( json )
    # return HttpResponse( res , mimetype='text/plain')





def approve_transit(request):
    """
    Performs ajaxy approval of a transit subsidy
    """

    #use request.user as signatore
    #fetch transit based on request.
    # uid = request.GET['user']
    # print uid
    #user = User.objects.get()
    # tran = TransitSubsidy.objects.filter(  )
    json = { 'approver':'Aprrover Name','approved_on':'2012-02-14 11:09 AM' }
    return JsonResponse( json )
    # return HttpResponse(uid)





#Below is eexperimental stuff



#Dump of raw JSON data. This should populate a form and allow Alex to check off as approved
def __approval_json(request):
    #Look at request.user for allowable staff
    staff = ( 'sheltonw@DO.TREAS.GOV' )
    #search staff for valid user
    if (False):
        return HttpResponse('[error]') 

    import itertools
    

    modes  = TransitSubsidyModes.objects.all()
    transits  = TransitSubsidy.objects.all()
    people = Person.objects.all()
    #, [ (mode) for mode in modes.filter(transit_subsidy_id=tran.user_id))
    

    bennies = [  (tran, tran.user, people.filter(user=tran.user)[0] ) for tran in transits ]
    chain =  itertools.chain(bennies)
    json = { 'page':'1', 'total':len(bennies), 'records': len(bennies), 'rows': list(chain) }
    # bennies = [  ( tran, tran.user, people.filter(user=tran.user)[0], [ (mode) for mode in modes.filter(transit_subsidy_id=tran.user_id) ] ) for tran in transits ]
    #bennies = [  { 'transit': tran, 'user':tran.user, 'user_profile':people.filter(user=tran.user)[0], 'modes':[ (mode) for mode in modes.filter(transit_subsidy_id=tran.user_id) ] } for tran in transits ]
    
    #chain =  itertools.chain(people)
    #import pdb;pdb.set_trace()
    
    return JsonResponse( json )


def approve_cool(request):
    # Distribution buckets, need to compute
    # TranBen , Smartrip, Regional, Other, TRANServe
    trans  = TransitSubsidy.objects.all()
    users  = User.objects.all()
    modes  = TransitSubsidyModes.objects.all()

    results = [ (user, user.transitsubsidy_set) for user in users ]

    approval = [ request.user.email, datetime.now() ]
    return JsonResponse( approval )

def approve(request):
    return render_to_response('transit_subsidy/approve.html',{},RequestContext(request))


@login_required
def old_approval_json(request):
    # Distribution buckets, need to compute
    # TranBen , Smartrip, Regional, Other, TRANServe
    res = u''
    json = { 'page': '0', 'total': '0' , 'records': '0', 'rows': [] }
    modes  = TransitSubsidyModes.objects.all()

    for trans in TransitSubsidy.objects.all():
        _tran_info = {}
        
        ts_modes = TransitSubsidyModes.objects.filter( transit_subsidy=trans )
        _tran_info['id'] = unicode(trans.user_id)
        _tran_info['username'] =  unicode(trans.user.username) 
        _tran_info['name'] = unicode(trans.user.last_name) +  ', ' + unicode(trans.user.first_name)
        _tran_info['total_commute_cost'] = unicode(trans.total_commute_cost)
        _tran_info['email'] = unicode(trans.user.email)
        _tran_info['total_amount'] =  unicode(trans.amount)
        _tran_info['last_four_ssn'] =  unicode(trans.last_four_ssn)
        _tran_info['date_enrolled'] =  unicode(trans.date_enrolled)
        _tran_info['timestamp'] =  unicode(trans.timestamp) 
        _tran_info['origin_address'] = unicode(trans.origin_street) + ' ' + unicode(trans.origin_city.encode('ascii','ignore') ) + ', ' +  unicode(trans.origin_state) + ' ' + unicode(trans.origin_zip) 
        _tran_info['destination'] =  unicode(trans.destination)
        _tran_info['workdays'] =  unicode(trans.number_of_workdays)
        _tran_info['daily_roundtrip_cost'] =  unicode(trans.daily_roundtrip_cost)
        _tran_info['daily_parking_cost'] =  unicode(trans.daily_parking_cost)
        _tran_info['smartrip_id'] =  unicode(trans.dc_wmta_smartrip_id)
        _tran_info['approved_by'] =  unicode(trans.approved_by)
        _tran_info['approved_on'] =  unicode(trans.approved_on)
        _tran_info['modes'] =   ts_modes  #[ (mode) for mode in modes.filter(id=trans.user_id) ]
        json['rows'].append(_tran_info)        
    return JsonResponse( json )






#Dump of raw JSON data. This should populate a form and allow Alex to check off as approved
def approval_json_comp(request):
    #Look at request.user for allowable staff
    staff = ( 'sheltonw@DO.TREAS.GOV' )
    #search staff for valid user
    if (False):
        return HttpResponse('[error]') 

    modes  = TransitSubsidyModes.objects.all()
    transits  = TransitSubsidy.objects.all()
    people = Person.objects.all()
    # bennies = [  ( tran, tran.user, people.filter(user=tran.user)[0], [ (mode) for mode in modes.filter(transit_subsidy_id=tran.user_id) ] ) for tran in transits ]
    bennies = [  { 'transit': tran, 'user':tran.user, 'user_profile':people.filter(user=tran.user)[0], 'modes':[ (mode) for mode in modes.filter(transit_subsidy=tran) ] } for tran in transits ]
    
    #chain =  itertools.chain(people)
    #import pdb;pdb.set_trace()
    
    return JsonResponse( bennies )

