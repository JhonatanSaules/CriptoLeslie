# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nube', '0002_auto_20171030_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cipher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100)),
                ('docfile', models.FileField(upload_to=b'cipher')),
            ],
        ),
    ]
