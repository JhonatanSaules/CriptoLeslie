# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nube', '0003_cipher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100)),
                ('docfile', models.FileField(upload_to=b'hash')),
            ],
        ),
    ]
