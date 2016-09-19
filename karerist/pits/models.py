# coding=utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

# Create your models here.

@python_2_unicode_compatible
class Pit(models.Model):

    name = models.CharField(_(u"Название"), max_length=255)
    org = models.ForeignKey('users.Org', verbose_name=_(u"Организация"))
    address = models.ForeignKey('users.Location', verbose_name=_(u"Адрес"))

    class Meta:
        verbose_name = _(u'Карьер')
        verbose_name_plural = _(u'Карьеры')
        unique_together = ('name', 'org')

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Material(models.Model):

    name = models.CharField(_(u"Название"), max_length=255, unique=True)

    class Meta:
        verbose_name = _(u'Материал')
        verbose_name_plural = _(u'Материалы')

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class PitMaterial(models.Model):

    pit = models.ForeignKey('pits.Pit', verbose_name=_(u"Карьер"))
    material = models.ForeignKey('pits.Material', verbose_name=_(u"Материал"))
    density = models.DecimalField(_(u"Плотность"), max_digits=10, decimal_places=3)
    fraction = models.CharField(_(u"Фракция"), max_length=255, blank=True, default='')
    solidity = models.CharField(_(u"Прочность"), max_length=255, blank=True, default='')
    price = models.DecimalField(_(u"Цена за метр кубический"), max_digits=20, decimal_places=2)
    capacity = models.DecimalField(_(u"Объем в день, м3"), max_digits=20, decimal_places=3)

    class Meta:
        verbose_name = _(u'Материал карьера')
        verbose_name_plural = _(u'Материалы карьеров')

    def __str__(self):
        return u"%s:%s" % (
            self.pit.name,
            self.material.name,
        )

    def price_ton(self):
        return self.price/self.density

@python_2_unicode_compatible
class Demand(models.Model):

    dt_created = models.DateTimeField(_(u"Дата/время создания"), auto_now_add=True)
    customer = models.ForeignKey('users.Org', verbose_name=_(u"Организация-заказчик"))
    material = models.ForeignKey('pits.Material', verbose_name=_(u"Материал"))
    fraction = models.CharField(_(u"Фракция"), max_length=255, blank=True, default='')
    solidity = models.CharField(_(u"Прочность"), max_length=255, blank=True, default='')
    volume = models.DecimalField(_(u"Объем"), max_digits=20, decimal_places=3)
    start_date = models.DateField(_(u"Дата начала"))
    end_date = models.DateField(_(u"Дата окончания"))
    address = models.ForeignKey('users.Location', verbose_name=_(u"Адрес доставки"))

    class Meta:
        verbose_name = _(u'Потребность в материале')
        verbose_name_plural = _(u'Потребности в материалах')
        ordering = ('dt_created', )

    def __str__(self):
        return u"%s:%s, %s - %s" % (
            self.customer.name,
            self.material.name,
            self.start_date,
            self.end_date,
        )

    def days_to_deliver(self):
        return (self.end_date - self.start_date).days + 1
