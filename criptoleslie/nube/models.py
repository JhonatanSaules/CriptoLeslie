from django.db import models


class Document(models.Model):
    filename = models.CharField(max_length=100)
    docfile = models.FileField(upload_to='documents')

class Cipher(models.Model):
    filename = models.CharField(max_length=100)
    docfile = models.FileField(upload_to='cipher')

class Hashes(models.Model):
    filename = models.CharField(max_length=100)
    docfile = models.FileField(upload_to='hash')