# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from users.models import Org

admin.site.register(Org)