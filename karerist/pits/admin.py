# -*- coding: utf-8 -*-

from django.contrib import admin

from pits.models import Pit, Material, PitMaterial, Demand

admin.site.register(Pit)
admin.site.register(Material)
admin.site.register(PitMaterial)
admin.site.register(Demand)
