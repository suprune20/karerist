# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 19:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr_str', models.CharField(blank=True, default=b'', max_length=255, verbose_name='\u0410\u0434\u0440\u0435\u0441')),
                ('lat', models.FloatField(verbose_name='\u0428\u0438\u0440\u043e\u0442\u0430')),
                ('lng', models.FloatField(verbose_name='\u0414\u043e\u043b\u0433\u043e\u0442\u0430')),
            ],
            options={
                'verbose_name': '\u0410\u0434\u0440\u0435\u0441',
                'verbose_name_plural': '\u0410\u0434\u0440\u0435\u0441\u0430',
            },
        ),
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'', max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u0438')),
                ('full_name', models.CharField(blank=True, default=b'', max_length=255, verbose_name='\u041f\u043e\u043b\u043d\u043e\u0435 \u043d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435')),
                ('description', models.TextField(blank=True, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435, \u043d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0434\u0435\u044f\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438')),
                ('inn', models.CharField(blank=True, default=b'', max_length=255, verbose_name='\u0418\u041d\u041d')),
                ('director', models.CharField(blank=True, default=b'', max_length=255, verbose_name='\u0414\u0438\u0440\u0435\u043a\u0442\u043e\u0440')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('phones', models.TextField(blank=True, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d\u044b')),
                ('fax', models.CharField(blank=True, default=b'', max_length=20, verbose_name='\u0424\u0430\u043a\u0441')),
                ('uses_vat', models.BooleanField(default=True, verbose_name='\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442 \u041d\u0414\u0421')),
            ],
            options={
                'verbose_name': '\u041e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f',
                'verbose_name_plural': '\u041e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u0438',
            },
        ),
    ]
