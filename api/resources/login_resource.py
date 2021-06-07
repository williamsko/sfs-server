from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.contrib.auth.models import User
from tastypie.serializers import Serializer
from entreprise.models import Agent, Entreprise, Key
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.fields import ForeignKey
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpAccepted


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser']


class AgentResource(ModelResource):

    class Meta:
        queryset = Agent.objects.all()
        list_allowed_methods = ['get', 'post', 'options']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'options']
        resource_name = 'agent'
        filtering = {
            'slug': ALL,
            'code': ALL,
            'user': ALL_WITH_RELATIONS,
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
        return super(AgentResource, self).determine_format(request)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r"^(?P<resource_name>%s)/key/activate%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('activate_key'), name="api_key_activation"),

        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body)
        username = data['username']
        password = data['password']
        try:
            user = User.objects.get(username=username)
            if user and user.is_active:
                result = user.check_password(password)
                if result:
                    agent = Agent.objects.get(informations=user)
                    bundle = self.build_bundle(obj=agent, request=request)
                    bundle = self.full_dehydrate(bundle)

                    entreprise = agent.entreprise
                    bundle.data.update(
                        {'entreprise': {'brand_name': entreprise.brand_name, 'code': entreprise.code}})
                    bundle.data.update({'response_code': '000'})
                    bundle.data.update({'first_name': user.first_name})
                    bundle.data.update({'last_name': user.last_name})

                    return self.create_response(request, bundle)
                else:
                    return self.create_response(request, {'response_text': 'wrong password', 'response_code': '100'}, HttpForbidden)
            else:
                return self.create_response(request, {'response_text': 'agent is not active', 'response_code': '100'}, HttpUnauthorized)
        except User.DoesNotExist:
            return self.create_response(request, {'response_text': 'unknwonw user', 'response_code': '100'}, HttpForbidden)

    
    def activate_key(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body)
        key = data['key']
        try:
            existing_key = Key.objects.get(key=key)
            if existing_key.status:
                return self.create_response(request, {'response_text': 'key already used', 'response_code': '100'}, HttpForbidden)

            existing_key.status = True
            existing_key.save()
            return self.create_response(request, {'response_text': 'OK'}, HttpAccepted)

        except Key.DoesNotExist:
            return self.create_response(request, {'response_text': 'unknown key', 'response_code': '100'}, HttpForbidden)
