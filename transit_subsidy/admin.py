from django.contrib  import admin
from transit_subsidy.models import TransitSubsidy,Mode,TransitSubsidyModes,OfficeLocation

class TransitSubsidyAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination','date_enrolled','timestamp')
    search_fields = ('user',)
    list_filter = ('destination',)
    ordering = ('user',)
    # exclude = ('last_four_ssn','date_enrolled')

class ModeAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'long_name','locality', 'url_link', 'distribution_method')
    search_fields = ('short_name', 'long_name','locality',)
    list_filter = ('locality',)
  
 

class TransitModesAdmin(admin.ModelAdmin):
        list_display = ('short_name', 'long_name','distribution_method')
        search_fields = ('short_name', 'long_name','distribution_method')
        list_filter = ('short_name', 'long_name','distribution_method')
        ordering = ('locality','short_name')
        
admin.site.register(TransitSubsidy,TransitSubsidyAdmin)
admin.site.register(Mode,ModeAdmin)
admin.site.register(TransitSubsidyModes)
admin.site.register(OfficeLocation)
