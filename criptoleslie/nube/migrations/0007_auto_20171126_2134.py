# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nube', '0006_auto_20171122_0607'),
    ]

    operations = [
        migrations.AddField(
            model_name='cipher',
            name='hash_c',
            field=models.CharField(default=b' ', max_length=100),
        ),
        migrations.AddField(
            model_name='cipher',
            name='user_name',
            field=models.CharField(default=b' ', max_length=100),
        ),
    ]
