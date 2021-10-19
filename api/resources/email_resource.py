from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.contrib.auth.models import User
from tastypie.serializers import Serializer
from entreprise.models import Entreprise
from reporting.models import Reporting

from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.fields import ForeignKey
from tastypie.http import HttpUnauthorized, HttpForbidden

import smtplib
import rstr
import PyPDF2

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate
from email.mime.text import MIMEText
from os.path import basename

from base64 import b64decode


class MultiPartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            _format = request.META.get('CONTENT_TYPE', 'application/json')
        elif format == 'application/x-www-form-urlencoded':
            return request.POST
        elif format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(MultiPartResource, self).deserialize(request, data, _format)


class EmailResource(MultiPartResource, ModelResource):

    class Meta:
        queryset = Reporting.objects.all()
        list_allowed_methods = ['get', 'post', 'options']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'options']
        resource_name = 'email'
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
        return super(EmailResource, self).determine_format(request)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/send%s$" %
                (self._meta.resource_name, trailing_slash()), self.wrap_view('send')),

        ]

    def send(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        try:
            data = self.deserialize(request, request.body)
            fiche_paie = data['fiche_paie'].split(',')[1]
            _bytes = b64decode(fiche_paie, validate=True)
            identifiant = data['identifiant']
            domain = data['domain']
            password = data['password']
            port = data['port']
            filename = data['filename']
            to = data['to']
            matricule = data['matricule']

            print (matricule)
            print (to)

            print('****************1*****************')

            path = f'{rstr.digits(6)}.pdf'
            outfile = open(path, 'wb')
            outfile.write(_bytes)
            outfile.close()

            print('****************2*****************')

            pdf_in_file = open(path, 'rb')
            inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
            pages_no = inputpdf.numPages

            for i in range(pages_no):
                print('****************ooo*****************')
                inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
                print('****************ooo*****************')
                output = PyPDF2.PdfFileWriter()
                print('****************ooo*****************')
                output.addPage(inputpdf.getPage(i))
                print('****************ooo*****************')
                output.encrypt(str(matricule))

            print('****************3*****************')

            with open(f'enc_{path}', 'wb') as outputStream:
                output.write(outputStream)

            print(f'enc_{path}')
            print('****************4*****************')
            byte_pdf = open(f'enc_{path}', 'rb')

            print('****************5*****************')

            msg = MIMEMultipart()
            msg['From'] = identifiant
            msg['To'] = COMMASPACE.join(to)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = 'Fiche de paie'
            msg.attach(MIMEText('HELLO'))
            part = MIMEApplication(byte_pdf.read(), Name='xx')
            part['Content-Disposition'] = f'attachment; filename="{filename}"'
            msg.attach(part)

            # smtp = smtplib.SMTP(domain)
            # smtp.login(identifiant, password)
            # smtp.sendmail(identifiant, to, msg.as_string())
            # smtp.close()
        except Exception as e:
            return self.create_response(request, {'error': e})

        return self.create_response(request, {'success': True})
