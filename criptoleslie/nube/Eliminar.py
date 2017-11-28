from random import randint
import socket
import hashlib
import hmac
import Crypto.Cipher.AES, Crypto.Util.Counter
import hmac
from rsagen import *
from Duplicidad import *
from django.core.files import File
from models import Hashes, Cipher


def eliminar_archivo(filename, nom_user):
    try:
        buscar = Cipher.objects.get(filename="c2_"+filename)
        var = buscar.filename
        #doc = File(buscar.docfile).read()

    except:
        var = ""
    print var
    print nom_user
    buscar = Cipher.objects.get(filename="c2_"+filename, user_name=nom_user)
    doc = buscar.hash_c
    print doc
    print buscar
    buscar.delete()
    try:
        buscar2 = Cipher.objects.filter(hash_c=doc).all()[1]
        print buscar2
    except:
        buscar2 = Cipher.objects.filter(hash_c=doc).all()[0]
        print buscar2
        buscar2.delete()
        buscar3 = Hashes.objects.get(hash_c=doc)
        buscar3.delete()
        print "eliminado"
