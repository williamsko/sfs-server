from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.contrib.auth.models import User
from tastypie.serializers import Serializer
from entreprise.models import SMTP, Entreprise
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.fields import ForeignKey
from tastypie.http import HttpUnauthorized, HttpForbidden


class SMTPResource(ModelResource):

    class Meta:
        queryset = SMTP.objects.all()
        list_allowed_methods = ['get', 'post', 'options']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'options']
        resource_name = 'smtp'
        filtering = {
            'slug': ALL,
            'entreprise': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        serializer = Serializer(
            formats=['json', 'jsonp', 'xml', 'yaml', 'plist'])

    def determine_format(self, request):
        """
        Used to determine the desired format from the request.format
        attribute.
        """
        if (hasattr(request, 'format') and request.format in self._meta.serializer.formats):
            return self._meta.serializer.get_mime_for_format(request.format)
        return super(SMTPResource, self).determine_format(request)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/create%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('create'), name="api_create"),

        ]

    def create(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body)
        identifiant = data['identifiant']
        password = data['password']
        domain = data['domain']
        port = data['port']
        entreprise_code = data['code_entreprise']

        try:
            smtp_param = SMTP.objects.get(entreprise__code=entreprise_code)
        except SMTP.DoesNotExist:
            smtp_param = SMTP()

        try:
            smtp_param.identifiant = identifiant
            smtp_param.password = password
            smtp_param.domain = domain
            smtp_param.port = port
            smtp_param.entreprise = Entreprise.objects.get(
                code=entreprise_code)
            smtp_param.save()
            return self.create_response(request, {'response_code': '000'})
        except Exception:
            return self.create_response(request, {'response_code': '-111'}, HttpForbidden)
       