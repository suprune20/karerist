# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-05 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pits', '0007_auto_20161005_1910'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pitload',
            options={'verbose_name': '\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u043a\u0430\u0440\u044c\u0435\u0440\u043e\u0432 (pitLoad)', 'verbose_name_plural': '\u0417\u0430\u0433\u0440\u0443\u043a\u0430 \u043a\u0430\u0440\u044c\u0435\u0440\u043e\u0432 (pitLoads)'},
        ),
        migrations.AddField(
            model_name='pitload',
            name='remains',
            field=models.PositiveIntegerField(default=0, verbose_name='\u041e\u0441\u0442\u0430\u043b\u043e\u0441\u044c \u043f\u0435\u0440\u0435\u0432\u0435\u0437\u0442\u0438 \u0433\u0440\u0443\u0437\u043e\u0432\u0438\u043a\u0430\u043c\u0438'),
            preserve_default=False,
        ),
    ]
