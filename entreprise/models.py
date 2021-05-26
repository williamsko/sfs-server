from django.db import models
import rstr
import slugify
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.


def entity_logo_directory_path(instance, filename):
    return f'entreprise_{slugify(instance.brand_name)}/logo.png'


class Entreprise(models.Model):

    code = models.CharField(
        unique=True,
        max_length=10,
        null=False,
        blank=False,
        default=rstr.digits(10),
    )

    brand_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.CharField(max_length=30, null=False, blank=False)
    phone_number = models.CharField(max_length=30, null=False, blank=False)
    address = models.CharField(max_length=50, null=False, blank=False)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    logo = models.ImageField(
        upload_to=entity_logo_directory_path, blank=True)

    def __str__(self):
        return self.brand_name

    class Meta:
        verbose_name = _("Entreprise")
        verbose_name_plural = _("Entreprises")
        app_label = 'entreprise'


class Agent(models.Model):

    matricule = models.CharField(
        unique=True,
        max_length=20,
        null=False,
        blank=False,
        default=rstr.digits(10),
    )
    informations = models.OneToOneField(User, on_delete=models.CASCADE)
    entreprise = models.ForeignKey(
        Entreprise, on_delete=models.DO_NOTHING, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.informations.first_name} {self.informations.last_name}'

    class Meta:
        verbose_name = _("Salarié")
        verbose_name_plural = _("Salariés")
        app_label = 'entreprise'


class SMTP(models.Model):
    entreprise = models.ForeignKey(
        Entreprise, on_delete=models.DO_NOTHING, null=True, blank=True)
    identifiant = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    domain = models.CharField(max_length=100, null=True, blank=True)
    port = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.domain}'

    class Meta:
        verbose_name = _('Param. SMTP')
        verbose_name_plural = _('Params. SMTP')
        app_label = 'entreprise'
