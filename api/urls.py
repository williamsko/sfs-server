from django.urls import path
from django.conf.urls import include
from tastypie.api import Api
from api.resources.login_resource import AgentResource
from api.resources.entreprise_resource import EntrepriseResource
from api.resources.param_smtp_resource import SMTPResource
from api.resources.reporting_resource import ReportingResource
from api.resources.email_resource import EmailResource


v1_api = Api(api_name='v1')


# Agent
v1_api.register(AgentResource())

# Entreprise
v1_api.register(EntrepriseResource())

# SMTP
v1_api.register(SMTPResource())

# Reporting
v1_api.register(ReportingResource())

# Email
v1_api.register(EmailResource())


urlpatterns = [
    path('api/', include(v1_api.urls)),
]
