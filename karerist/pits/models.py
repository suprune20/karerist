# coding=utf-8

from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db.models.query_utils import Q

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
    density = models.DecimalField(_(u"Плотность"), max_digits=8, decimal_places=2)
    fraction = models.CharField(_(u"Фракция"), max_length=255, blank=True, default='')
    solidity = models.CharField(_(u"Прочность"), max_length=255, blank=True, default='')
    price = models.DecimalField(_(u"Цена за метр кубический"), max_digits=20, decimal_places=2)
    capacity = models.PositiveIntegerField(_(u"Объем в день, м3"))

    class Meta:
        verbose_name = _(u'Материал карьера')
        verbose_name_plural = _(u'Материалы карьеров')
        unique_together = ('pit', 'material', 'fraction', 'solidity',)

    def __str__(self):
        return u"%s:%s" % (
            self.pit.name,
            self.material_str(),
        )

    def price_ton(self):
        return self.price/self.density

    def material_str(self):
        result = u"%s" % self.material.name
        if self.fraction:
            result += u", фр. %s" % self.fraction
        if self.solidity:
            result += u", пр. %s" % self.solidity
        return result

@python_2_unicode_compatible
class Demand(models.Model):
    MSG_INVALID_DAYS = _(u"Дата начала больше даты окончания")

    dt_created = models.DateTimeField(_(u"Дата/время создания"), auto_now_add=True)
    customer = models.ForeignKey('users.Org', verbose_name=_(u"Организация-заказчик"))
    material = models.ForeignKey('pits.Material', verbose_name=_(u"Материал"))
    fraction = models.CharField(_(u"Фракция"), max_length=255, blank=True, default='')
    solidity = models.CharField(_(u"Прочность"), max_length=255, blank=True, default='')
    volume = models.PositiveIntegerField(_(u"Объем"))
    start_date = models.DateField(_(u"Дата начала"))
    end_date = models.DateField(_(u"Дата окончания"))
    address = models.ForeignKey('users.Location', verbose_name=_(u"Адрес доставки"))

    class Meta:
        verbose_name = _(u'Потребность в материале')
        verbose_name_plural = _(u'Потребности в материалах')
        ordering = ('dt_created', )

    def __str__(self):
        return u"%s:%s, %s кбм, %s - %s" % (
            self.customer.name,
            self.material.name,
            self.volume,
            self.start_date,
            self.end_date,
        )

    def dates_to_deliver(self):
        if self.end_date < self.start_date:
            raise ValueError(self.MSG_INVALID_DAYS)
        date = self.start_date
        result = [date, ]
        while date < self.end_date:
            date += datetime.timedelta(days=1)
            result.append(date)
        return result

    def date_volumes(self):
        """
        Сколько нужно поставлять по дням

        dict(date=..., volume=...)
        """
        dates = self.dates_to_deliver()
        n_days = len(dates)
        average = self.volume // n_days
        result = [dict(date=d, volume=average) for d in dates]
        # Не всегда потребность распределятся нацело на дни
        # Путь self.volume = 8, а дней - 3. Делим нацело, на каждый день 2
        # 2*3 = 6. Надо раскидать оставшиеся 2 по дням, так чтобы
        # 1-й день: 3, 2-й день: 3, 3-й день: 2
        diff = average * n_days - self.volume
        diff_d = diff
        i = 0
        while diff_d < 0:
            result[i]['volume'] += 1
            i += 1
            diff_d += 1
        return result

    def pits_available_all(self):
        """
        Список карьеров потребности, с затребованным материалом, сортированный по расстоянию

        dict(pit=pit, pitmaterial=pitmaterial, distance=distance)
        """
        pms = [ (pm, pm.pit,) for pm in PitMaterial.objects.filter(
                    material=self.material,
                    fraction=self.fraction,
                    solidity=self.solidity,
        )]
        result = [ dict(pit=pm[1], pitmaterial=pm[0], distance=self.address.distance_to(pm[1].address)) \
                    for pm in pms ]
        return sorted(result, key=lambda result_dict: result_dict['distance'])

@python_2_unicode_compatible
class PitLoad(models.Model):

    dt_created = models.DateTimeField(_(u"Дата/время создания"), auto_now_add=True)
    date = models.DateField(_(u"Дата"))
    demand = models.ForeignKey('pits.Demand', verbose_name=_(u"Потребность"))
    pitmaterial = models.ForeignKey('pits.PitMaterial', verbose_name=_(u"Материал карьера"))
    volume = models.PositiveIntegerField(_(u"Объем за дату"))

    class Meta:
        verbose_name = _(u'Загрука карьеров')
        verbose_name_plural = _(u'Загрука карьеров')

    def __str__(self):
        return u"%s" % self.dt_created

@python_2_unicode_compatible
class PitRemain(models.Model):

    dt_created = models.DateTimeField(_(u"Дата/время создания"), auto_now_add=True)
    date = models.DateField(_(u"Дата"))
    pitmaterial = models.ForeignKey('pits.PitMaterial', verbose_name=_(u"Материал карьера"))
    volume = models.PositiveIntegerField(_(u"Остаток за дату"))

    class Meta:
        verbose_name = _(u'Остатки по карьерам')
        verbose_name_plural = _(u'Остатки по карьерам')

    def __str__(self):
        return u"%s" % self.dt_created
