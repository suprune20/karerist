# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from users.models import Org, Profile, Location

admin.site.register(Org)
admin.site.register(Profile)
admin.site.register(Location)
