from django.db import models


class Document(models.Model):
    docfile = models.FileField(upload_to='documents')

class Cipher(models.Model):
    filename = models.CharField(max_length=100)
    hash_c = models.CharField(max_length=100, default=' ')
    user_name = models.CharField(max_length=100, default=' ')
    docfile = models.FileField(upload_to='cipher')

class Hashes(models.Model):
    filename = models.CharField(max_length=100)
    hash_c = models.CharField(max_length=100, default=' ')
    docfile = models.FileField(upload_to='hash')
