# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predict_house_prices', '0002_auto_20150220_0021'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Clusters',
            new_name='Cluster',
        ),
    ]
