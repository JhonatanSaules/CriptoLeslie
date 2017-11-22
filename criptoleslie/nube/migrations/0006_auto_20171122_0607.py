# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nube', '0005_hashes_hash_c'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashes',
            name='hash_c',
            field=models.CharField(default=b' ', max_length=100),
        ),
    ]
