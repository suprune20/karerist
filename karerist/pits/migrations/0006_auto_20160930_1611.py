# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 16:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('pits', '0005_auto_20160921_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('capacity', models.PositiveIntegerField(verbose_name='\u0412\u043c\u0435\u0441\u0442\u0438\u043c\u043e\u0441\u0442\u044c, \u043a\u0431\u043c')),
                ('trips', models.PositiveIntegerField(verbose_name='\u0427\u0438\u0441\u043b\u043e \u0440\u0435\u0439\u0441\u043e\u0432 \u0432\u0434\u0435\u043d\u044c')),
                ('price_tcbm', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='\u0426\u0435\u043d\u0430 \u0437\u0430 \u0442\u043e\u043d\u043d\u043e-\u043a\u0438\u043b\u043e\u043c\u0435\u0442\u0440')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Org', verbose_name='\u041e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f')),
            ],
            options={
                'verbose_name': '\u0413\u0440\u0443\u0437\u043e\u0432\u0438\u043a',
                'verbose_name_plural': '\u0413\u0440\u0443\u0437\u043e\u0432\u0438\u043a\u0438',
            },
        ),
        migrations.AlterModelOptions(
            name='pitload',
            options={'verbose_name': '\u0417\u0430\u0433\u0440\u0443\u043a\u0430 \u043a\u0430\u0440\u044c\u0435\u0440\u043e\u0432', 'verbose_name_plural': '\u0417\u0430\u0433\u0440\u0443\u043a\u0430 \u043a\u0430\u0440\u044c\u0435\u0440\u043e\u0432'},
        ),
        migrations.AlterModelOptions(
            name='pitremain',
            options={'verbose_name': '\u041e\u0441\u0442\u0430\u0442\u043a\u0438 \u043f\u043e \u043a\u0430\u0440\u044c\u0435\u0440\u0430\u043c', 'verbose_name_plural': '\u041e\u0441\u0442\u0430\u0442\u043a\u0438 \u043f\u043e \u043a\u0430\u0440\u044c\u0435\u0440\u0430\u043c'},
        ),
        migrations.AlterUniqueTogether(
            name='truck',
            unique_together=set([('name', 'org')]),
        ),
    ]
