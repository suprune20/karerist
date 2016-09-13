# -*- coding: utf-8 -*-
from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

@python_2_unicode_compatible
class Org(models.Model):

    TYPE_SUPPLIER = 'supplier'
    TYPE_TRANSPORTER = 'transporter'
    TYPE_CUSTOMER = 'customer'
    TYPE_SUPERVISOR = 'supervisor'
    ORG_TYPES = (
        (TYPE_SUPPLIER, _(u"Поставщик")),
        (TYPE_TRANSPORTER, _(u"Перевозчик")),
        (TYPE_CUSTOMER, _(u"Заказчик")),
        (TYPE_SUPERVISOR, _(u"Заказчик")),
    )

    
    type = models.CharField(_(u"Тип"), max_length=255, choices=ORG_TYPES)
    name = models.CharField(_(u"Название организации"), max_length=255, default='')
    full_name = models.CharField(_(u"Полное наименование"), max_length=255, default='', blank=True)
    description = models.TextField(_(u"Описание, направление деятельности"), blank=True, null=True)
    inn = models.CharField(_(u"ИНН"), max_length=255, default='', blank=True)
    director = models.CharField(_(u"Директор"),
                                max_length=255, default='', blank=True)
    email = models.EmailField(_(u"Email"), blank=True)
    phones = models.TextField(_(u"Телефоны"), blank=True, null=True)
    fax = models.CharField(_(u"Факс"), max_length=20, default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Организация')
        verbose_name_plural = _(u'Организации')
