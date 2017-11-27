# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nube', '0007_auto_20171126_2134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='filename',
        ),
    ]
