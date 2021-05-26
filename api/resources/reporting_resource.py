from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.contrib.auth.models import User
from tastypie.serializers import Serializer
from entreprise.models import Entreprise
from reporting.models import Reporting

from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.fields import ForeignKey
from tastypie.http import HttpUnauthorized, HttpForbidden


class ReportingResource(ModelResource):

    class Meta:
        queryset = Reporting.objects.all()
        list_allowed_methods = ['get', 'post', 'options']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'options']
        resource_name = 'reporting'
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
        return super(ReportingResource, self).determine_format(request)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/create%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('create'), name="api_create"),

        ]

    def create(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body)
        start_date = data['start_date']
        end_date = data['end_date']
        entreprise_code = data['code_entreprise']

        try:
            reporting = Reporting()
            reporting.start_date = start_date
            reporting.end_date = end_date
            reporting.entreprise = Entreprise.objects.get(
                code=entreprise_code)
            reporting.save()

            return self.create_response(request, {'response_code': '000'})
        except Exception:
            return self.create_response(request, {'response_code': '-111'}, HttpForbidden)
