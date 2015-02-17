# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=1000)),
                ('state', models.CharField(max_length=1000)),
                ('median_income', models.FloatField()),
                ('population_density', models.FloatField()),
                ('median_household_value', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(max_length=1000)),
                ('city', models.CharField(max_length=1000)),
                ('zip_code', models.CharField(max_length=1000)),
                ('state', models.CharField(max_length=1000)),
                ('house_type', models.CharField(max_length=1000)),
                ('sale_date', models.CharField(max_length=1000)),
                ('beds', models.IntegerField()),
                ('baths', models.IntegerField()),
                ('square_feet', models.IntegerField(null=True)),
                ('actual_price', models.FloatField()),
                ('predicted_price', models.FloatField(null=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
