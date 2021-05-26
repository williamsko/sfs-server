from django.db import models
import rstr
from entreprise.models import Entreprise, Agent
from django.utils.translation import ugettext_lazy as _


class Reporting(models.Model):

    code = models.CharField(
        unique=True,
        max_length=10,
        null=False,
        blank=False,
        default=rstr.digits(10),
    )

    status = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey(
        Entreprise, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        verbose_name = _("Rapport")
        verbose_name_plural = _("Rapports")
        app_label = 'reporting'


class MailingList(models.Model):
    reporting = models.ForeignKey(
        'Reporting', on_delete=models.DO_NOTHING, null=False, blank=False)
    salarie = models.ForeignKey(
        Agent, on_delete=models.DO_NOTHING, null=True, blank=True)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.informations.first_name} {self.informations.last_name}'

    class Meta:
        verbose_name = _("Mailing list")
        verbose_name_plural = _("Mailing list")
        app_label = 'reporting'
