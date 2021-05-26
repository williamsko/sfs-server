from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.contrib.auth.models import User
from tastypie.serializers import Serializer
from entreprise.models import Entreprise
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.fields import ForeignKey
from tastypie.http import HttpUnauthorized, HttpForbidden


class EntrepriseResource(ModelResource):

    class Meta:
        queryset = Entreprise.objects.all()
        list_allowed_methods = ['get', 'post', 'options']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'options']
        resource_name = 'entreprise'
        filtering = {
            'slug': ALL,
            'code': ALL,
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
        return super(EntrepriseResource, self).determine_format(request)

    