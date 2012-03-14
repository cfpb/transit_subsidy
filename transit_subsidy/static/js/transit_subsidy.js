/**
 * Transit Subsidy JavaScript
 *
 * @author bill shelton
 * @version 1.01
 *
 * @date 9.18.11
 * 
 * */


$.validator.addMethod("segment_amount", function(value, element) {
   // return true;
   
   var sel_id = 'segment-type_' + element.id.split('_')[1];
   var sel = $('#' + sel_id )
   var sel_val = sel.val();
   //$(sel).rules( 'add', 'required' );
   //$('#' + element.id).rules( 'add', {required:true} );
   // console.log( element.id );
   if (sel_val == '') return false;
   var rx = /^\d*\.?((25)|(50)|(5)|(75)|(0)|(00))?$/g;
   if ( element.value == '' ) return false;   
   return true;
 }, "Select a segment and enter an amount.");


$.validator.addMethod("smartrip_id", function(value, element) {
   //For each segment_type element, if the selected on is in the list
   //of smartrips AND element is empty, return false
   //Note, segment_data is fetched via ajax from server, so, in theory
   //it's current.

   //Minimum length
   if( value.length >= 9 ) return true;
   _retval = true;

   //generate a list of Smartip ids
   var smartrips = $.map( segment_data, function(item){
     if (item['distribution_method'] == 'Smartrip') return item['id'];
   });
   // console.log(smartrips);
   $('.seg').each( function(i,element){
      smart_id =  parseInt( $(element).val() );//element[element.selectedIndex].value;
      _index = $.inArray(smart_id, smartrips)
      if( _index > -1)  { 
        _retval = false;
        return false; //Note that this returns from each() NOT the method
      } 
   });
   return _retval;
 }, "Enter your Smartip card number.");



MAX_AMT = 125;

function compute_totals() {
    var rt = parseFloat($('#id_daily_roundtrip_cost').val());
    var days = parseFloat($('#id_number_of_workdays').val());
    var total_cost =   rt * days;
    if( isNaN( total_cost) ) total_cost = 0;
    $("#id_total_commute_cost").val(total_cost.toFixed(2));
    var _total = (total_cost > MAX_AMT ? MAX_AMT : total_cost);
    $("#id_amount").val(_total.toFixed(2));
}



/**
 *
 *  Methods for creating dynamic form elements. Specifically, commuting segments.
 */
var add_commuting_segments = function(){
    var current_element_id = segment_id; //e.g., current -d == 1
    segment_id++; //e.g., next id == 2
    //Simply replace all occurance of {0} with the value of segment_id, which should be 1..N,
    //and use that to create the id for the injected form elements.
    var new_formelements = segments_template.replace(/\{0\}/g, current_element_id)
    //console.log(new_formelements); //replaced html to append
    $(new_formelements).appendTo("#commuting_segments tbody");
    var sel_id = '#segment-type_' + current_element_id;
    $(segment_data).each(  function(i,o) {
      $(sel_id).append( '<option value="' + o.id + '">' + o.short_name + ' &mdash; ' + o.locality +'</option>'  );
    }); 
  }
 

segments_template = $("#template").val();
segment_id = 1;
    

segment_data = [ ]; 

$.ajaxSetup({async:false});
$.post('modes', function(res){
   segment_data = res;
});

  
$(document).ready( function(){

  $("#colorbox").appendTo('form:first');


  init();
  add_commuting_segments();
 

  $("input[name='work_sked']").click(function() {
    switch ($(this).val()) {
  	case "8": $("#id_number_of_workdays").val("17");
  			  break;
  	case "9": $("#id_number_of_workdays").val("19");
  			  break;
  	case "10": $("#id_number_of_workdays").val("21");
  			   break;
  	default: $("#id_number_of_workdays").val("");
  			 break;
    }
    compute_totals();
  });



  $("#colorbox").appendTo('#frm_smartrip');
 


  /**
   * Implements Text Field Hints using labels so as not to mess up validation
   * */
  $('label.infield').inFieldLabels();


  /**
  */
  $(".add").live('click', function(){
    var sel_id = $("select[id^=segment-type]:last").attr('id');
    var id_num = sel_id.split('_')[1];
    add_commuting_segments();    
  }); 

   
  
  $('.rm').live('click', function() {
      
      //Make sure not to remove the last one.
      var how_many = $('.segment_row').size(); 
      if (how_many == 1) return;

      var counter = this.id.split('_')[1]
      if (counter <= 1) return;  //shouldn't remove the first and only element set
      $('#row_' + counter).remove();
      $('#subrow_' + counter).remove();

      //Make sure to re-compute the totals
      compute_daily_one_ways();
  });


  $('.seg').live( 'change', function(){
    var selected = $(this).val();
    var tid = this.id.split('_')[1];
    // console.log( '#other-segment_' + tid );
    if(selected == 9 || selected == -1) {
      $('#segment-other_' + tid).show('fast');
      $('#segment-other_' + tid).focus();
    }
    else {
      $('#segment-other_' + tid).val('');
      $('#segment-other_' + tid).hide('fast');  
    } 
  });



   var compute_daily_one_ways = function(){
     var totals = 0;
     $("#commuting_segments input.segment_amount").each(function() {
       var num;
       if( !isNaN( num = parseFloat(this.value)) )  totals += num;
     });
    
     $("#totals").attr("value", totals.toFixed(2) );//.valid();
     var _daily_rt = totals * 2;
     $("#id_daily_roundtrip_cost").val( _daily_rt.toFixed(2) );
     
     $("#frm_smartrip").validate().element( "#commuting_segments input.segment_amount" );
     compute_totals();
   }


  
  //TO DO; Instead of listening to entire form, listen to specific elements
  $(".segment_amount").live("keyup", function(event) {
    compute_daily_one_ways();
  });



  /**
   * Main validation.  The challenge was to combine the validation on multiple fields
   * into a single message.  This was done to support layout requirements.
   *
   * */

    $('#frm_smartrip').validate({
      //if debug is true, submit will be disbaled
      //debug: true,
      errorElement: 'em',
      errorPlacement: function(error, element) {
          element_id = element.get(0).id;
          // console.log( element_id );
          error.css("margin", "0 0 0 10px");

          if( element_id == 'id_origin_street'||
              element_id == 'id_origin_city'||
              element_id == 'id_origin_state'||
              element_id == 'id_origin_zip'
              ){
              $('#id_orig_errors').html( error.get(0) ) ;
             // $('#id_orig_errors').addClass('error')
          }
          else if(element_id.indexOf('segment-amount') != -1 ) {
              var _eid = element_id.split('_')[1];
              error.insertAfter( $('#segment-amount_' + _eid + '_error') );
          }
          else if(element_id == 'id_work_sked'){
              error.insertBefore( $('#id_work_sked_error') );
          }
          else if(element_id == 'id_destination'){
              error.insertAfter( $('#id_destination_error') );
          }
          else if(element_id == 'id_route_description'){
              error.insertAfter( $('#id_route_description_error') );
          }
          else {
              error.insertAfter(element);
          }
      },
      success: function(label) {
          var eid = label.attr('for');
          //console.log(eid + ' OK');
          if( eid == 'id_first_name' ||
              eid == 'id_last_name' ||
              eid == 'id_email')  {
              label.removeClass('error');
              label.addClass('cancel');
          } 
          else if ( eid.indexOf('segment-amount') != -1 ) {
              label.removeClass('error');
              label.addClass('cancel');
          }                       
          else {
              label.removeClass('error');
              label.addClass("success");
          }

      },
      rules: {
         work_sked: {
           required: true
         },
         totals: {
           required: false
         },
         last_four_ssn: {
            required: true,
            minlength: 4,
            maxlength: 4,
            digits: true
         },
         first_name: {
             required: false
         },
         last_name: {
             required: false
         },
         email: {
             required: false
         },
         origin_street:{
             required: true
         },
         origin_city: {
             required: true
         },
         origin_zip: {
             required: true,
             minlength: 5,
             maxlength: 5,
             digits: true
         },
         origin_state: {
             required: true,
             minlength: 2,
             maxlength: 2
         },
         destination: {
             required: true
         },
         number_of_workdays: {
              required:true,
              range: [1,31],
              number:true
         },
         amount: {
              required:true,
              range: [1,MAX_AMT],
              number:true
          },
          daily_roundtrip_cost: {
              required: false,
              number: true
          },
         signature: 'required'
      },
      messages: {
         last_four_ssn: 'We need the last 4 digits of your SSN',
         signature: 'Type you name as your signature.',
         //The origin_* items are the same because of the errorPlacement requirements.
         //That is, there is only to be one error message for all items, but
          // all items need to be validated.
         origin_street: 'We need your home address (Street, City, State, Zip)',
         origin_city: 'We need your home address (Street, City, State, Zip)',
         origin_state: 'We need your home address (Street, City, State, Zip)',
         origin_zip: 'We need your home address (Street, City, State, Zip)',

         destination: 'You must select your office location',
         number_of_workdays: 'Select at least one work schedule option above',
         daily_roundtrip_cost: 'The approximate cost for <em>one</emd> round-trip fair',
         amount: 'Specify commuting segments, costs, and work schedule',
         work_sked: 'Please select one work schedule option'
      }
    });
    

    $('#id_number_of_workdays').blur(function() {
      compute_totals();
    });


      /**
      * Generates a link for Google Transit based on origin and destination, and
      * opens a new window to Google Transit.
      * */
     $('#ln_estimate_trip').click(function(){
         street = $('#id_origin_street').val();
         city = $('#id_origin_city').val();
         state = $('#id_origin_state').val();
         zip = $('#id_origin_zip').val();
         orig = street + ', ' + city + ' ' + state + ', ' + zip;
         dest = $('#id_destination option:selected').text();
         u = 'http://www.google.com/maps?ie=UTF8&f=d&dirflg=r&hl=en&saddr=' + orig + '&daddr=' + dest + '&ttype=dep';
         window.open(u,'_blank')
     });


      /**
      * Generates a link to transit tools based on the office selection
      * */
    $('#id_destination').change(function(){
         //Should look like this
         //DC1800,DC1700,DC1750,DC820,CH200,NY330,SF4
         var location_id = $('#id_destination  option:selected').val();
         if(location_id == '' ) {
             $('#transit_tools').html('');
             return;
         }
         var city_abbrev = location_id.substr(0,2);
         $('#transit_tools').html( '<span style="color: #0c821a;">|</span>&nbsp;&nbsp; Trip planner for: '  + transit_tool_links[city_abbrev] );
    });




    /**
    * Displays modal dialog for the Transit Subsidy Policy
    * */
    $('#btn_enroll_smartrip').click( function(){
          var is_valid = $('#frm_smartrip').valid();
          if(is_valid) {
              $.colorbox({ 
              title: 'Transit Subsidy Program Applicant Agreement Statement',
              width:'65%',
              height: '65%',
              html: $('#tos').html() 
            }); 
		        $("#tos_wrapper").show();
          }
     });
    



    /**
    * Displays modal dialog for the transportation modes
    * */
    $('.ex_link').colorbox({
       html: $('#id_examples').html()
    });

    /**
    * Displays modal dialog for the Transit Tools
    * */
    $('#id_commuter_tools').colorbox({
       width: '420px',
       html: $('#id_transit_tool_wrapper').html()
    });


    /**
    * Displays modal dialog for the Transit Tools
    * */
    $('#id_cancel_enrollment').colorbox({
       width: '420px',
       html: $('#id_withdrawl_dialog').html()
    });


    $('#id_body').keyup( function( e ){
		// console.log(e)
        if(e.srcElement.id != 'id_body') return;
        var code = (e.keyCode ? e.keyCode : e.which);
        Q_KEY = 191; // '?'
        if(e.shiftKey && e.which == Q_KEY){
            //console.log(e)
            $.colorbox({
                width: 580,
                height: 420,
                html: $('#id_help').html()
            });
          //e.stopPropagation() = true;
        }
    });

  $('#id_help_smartrip').colorbox({
       html: $('#help_for_smartrip_card').html(),
       width: 500,
       height: 520
    });


 }); //end $



/**
 * Initializes form fields with constraints and styles.
 * */
  function init(){
    //Should be placed in initialization method
     //Tweaking form fields because Django won't
     $('body').attr({'id': 'id_body'});
	   $('#id_last_four_ssn').attr({'maxlength':4, 'autocomplete':false}).focus();
     $('#id_number_of_workdays').attr({'maxlength':2});
     $('#id_origin_state').attr({'maxlength':2});
     $('#id_origin_zip').attr({'maxlength':5});
     $('#id_amount').attr({'maxlength':6, 'autocomplete':false});
     $('#id_amount').addClass('no_border');
     $('#id_amount').attr({'readonly':true});
     $('#id_total_commute_cost').attr({'readonly':true});
     $('#id_total_commute_cost').addClass('no_border');
     $('#id_daily_roundtrip_cost').attr({'maxlength':6,'readonly':true});
     $('#id_daily_roundtrip_cost').addClass('no_border');     
     $('#id_first_name').addClass('no_border');
     $('#id_last_name').addClass('no_border');
     $('#id_email').addClass('no_border');
     $('#id_destination option:eq(0)').replaceWith('<option style="color:#777" value=""> &mdash;&mdash;&mdash;  Select your office location &mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;</option>');
     $('#id_dc_wmta_smartrip_id').addClass('smartrip_id');     
  }


  /**
   * Links for public transportation site tools
   * */
   var transit_tool_links = {
        'DC': '<a href="http://www.wmata.com/rider_tools/tripplanner/tripplanner_form_solo.cfm" target="_blank"> WMATA (DC)</a>',
        'SF': '<a href="http://www.bart.gov/tickets/calculator/index.aspx" target="_blank">BART (SF)</a>',
        'NY': '<a href="http://tripplanner.mta.info/MyTrip/ui_web/customplanner/TripPlanner.aspx" target="_blank">MTA (NY)</a>',
        'CH': '<a href="http://www.transitchicago.com/travel_information/trip_planner.aspx" target="_blank">CTA (Chicago)</a>'
   };
