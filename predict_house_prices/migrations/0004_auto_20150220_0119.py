# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predict_house_prices', '0003_auto_20150220_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cluster',
            name='index',
            field=models.CharField(max_length=10, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='house',
            name='cluster',
            field=models.CharField(max_length=10, blank=True),
            preserve_default=True,
        ),
    ]
