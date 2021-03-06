from django.contrib import admin
from entreprise.models import Entreprise, Agent, SMTP, Key, AdminPassword
# Register your models here.


class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'email', 'address', 'phone_number', 'status')
    search_fields = ['brand_name']


admin.site.register(Entreprise, EntrepriseAdmin)


class AgentAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'email', 'address', 'phone_number', 'status')
    search_fields = ['matricule', 'phone_number', 'email']


admin.site.register(Agent, AgentAdmin)


class SMTPAdmin(admin.ModelAdmin):
    list_display = ('entreprise', 'identifiant', 'domain', 'port', 'status')
    search_fields = ['entreprise__brand_name', 'identifiant', 'domaine']


admin.site.register(SMTP, SMTPAdmin)


class KeyAdmin(admin.ModelAdmin):
    list_display = ('content', 'entreprise', 'status')
    search_fields = ['entreprise', 'status']


admin.site.register(Key, KeyAdmin)


class AdminPasswordAdmin(admin.ModelAdmin):
    list_display = ('key', 'identifiant', 'password')
    search_fields = ['identifiant', 'status']


admin.site.register(AdminPassword, AdminPasswordAdmin)
