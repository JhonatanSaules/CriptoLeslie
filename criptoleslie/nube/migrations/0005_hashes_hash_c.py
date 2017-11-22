# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nube', '0004_hashes'),
    ]

    operations = [
        migrations.AddField(
            model_name='hashes',
            name='hash_c',
            field=models.TextField(default=b' ', max_length=100),
        ),
    ]
