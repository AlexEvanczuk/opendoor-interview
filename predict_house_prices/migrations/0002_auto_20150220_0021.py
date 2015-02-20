# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predict_house_prices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clusters',
            fields=[
                ('index', models.IntegerField(serialize=False, primary_key=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'Cities'},
        ),
        migrations.AddField(
            model_name='house',
            name='cluster',
            field=models.IntegerField(default=1, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='city',
            name='median_household_value',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='city',
            name='median_income',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='city',
            name='population_density',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
