# -*- coding: utf-8 -*-

from LatLon import LatLon, Latitude, Longitude

from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from karerist.utils import capitalize

@python_2_unicode_compatible
class Org(models.Model):

    name = models.CharField(_(u"Название организации"), max_length=255, default='')
    full_name = models.CharField(_(u"Полное наименование"), max_length=255, default='', blank=True)
    description = models.TextField(_(u"Описание, направление деятельности"), blank=True, null=True)
    inn = models.CharField(_(u"ИНН"), max_length=255, default='', blank=True)
    director = models.CharField(_(u"Директор"),
                                max_length=255, default='', blank=True)
    email = models.EmailField(_(u"Email"), blank=True)
    phones = models.TextField(_(u"Телефоны"), blank=True, null=True)
    fax = models.CharField(_(u"Факс"), max_length=20, default='', blank=True)
    uses_vat = models.BooleanField(_(u"Использует НДС"), default=True)

    class Meta:
        verbose_name = _(u'Организация')
        verbose_name_plural = _(u'Организации')

    def __str__(self):
        return self.name

    def is_supervisor(self):
        return str(self.pk) == str(settings.ORG_SUPERVISOR_PK)

@python_2_unicode_compatible
class Profile(models.Model):

    user = models.OneToOneField('auth.User')
    org = models.ForeignKey('users.Org')
    last_name = models.CharField(_(u"Фамилия"), max_length=255, )
    first_name = models.CharField(_(u"Имя"), max_length=255, blank=True, default='')
    middle_name = models.CharField(_(u"Отчество"), max_length=255, blank=True, default='')
    phones = models.TextField(_(u"Телефон(ы)"), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Профиль')
        verbose_name_plural = _(u'Профили')
        ordering = ('last_name', 'first_name', 'middle_name', )

    def __str__(self):
        return self.full_name() or self.user.username or u'%s' % self.pk

    def full_name(self, put_middle_name=True):
        name = ""
        if self.last_name:
            name = self.last_name
            if self.first_name:
                name = u"{0} {1}".format(name, self.first_name)
                if put_middle_name and self.middle_name:
                    name = u"{0} {1}".format(name, self.middle_name)
        if not name:
            name = self.user.username
        return name

    def last_name_initials(self):
        """
        Фамилия И.О.
        """
        name = ""
        if self.last_name:
            name = self.last_name
            if self.first_name:
                name = u"{0} {1}.".format(name, self.first_name[0])
                if self.middle_name:
                    name = u"{0}{1}.".format(name, self.middle_name[0])
        return name or self.user.username

    def save(self, *args, **kwargs):
        self.first_name = capitalize(self.first_name)
        self.last_name = capitalize(self.last_name)
        self.middle_name = capitalize(self.middle_name)
        return super(Profile, self).save(*args, **kwargs)

@python_2_unicode_compatible
class Location(models.Model):

    addr_str = models.CharField(_(u"Адрес"), max_length=255, blank=True, default='')
    lat = models.FloatField(_(u"Широта"))
    lng = models.FloatField(_(u"Долгота"))

    class Meta:
        verbose_name = _(u'Адрес')
        verbose_name_plural = _(u'Адреса')

    def __str__(self):
        if self.addr_str:
            return self.addr_str
        else:
            return _(u"Широта %(lat)s, долгота %(lng)s") % dict(
                lat=self.lat,
                lng=self.lng,
            )

    def distance_direct_to(self, location):
        """
        Расстояние по прямой до другого Location в км с округление до метра
        """
        this_loc = LatLon(Latitude(self.lat), Longitude(self.lng))
        other_loc = LatLon(Latitude(location.lat), Longitude(location.lng))
        return round(this_loc.distance(other_loc), 3)

    # Пока не сделали рассояние по дорогам, пусть будет так:
    distance_to = distance_direct_to
