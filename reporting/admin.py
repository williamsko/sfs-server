from django.contrib import admin
from reporting.models import Reporting, MailingList
# Register your models here.


class ReportingAdmin(admin.ModelAdmin):
    list_display = ('entreprise', 'start_date', 'end_date', 'status')
    search_fields = ['entreprise__brand_name']


admin.site.register(Reporting, ReportingAdmin)


class MailingListAdmin(admin.ModelAdmin):
    list_display = ('reporting', 'salarie', 'created', 'status')
    search_fields = ['salarie']


admin.site.register(MailingList, MailingListAdmin)
