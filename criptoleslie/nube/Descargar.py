from random import randint
import socket
import hashlib
import hmac
import Crypto.Cipher.AES, Crypto.Util.Counter
import hmac
from rsagen import *
from Duplicidad import *
from django.core.files import File
from models import Hashes,Cipher


def descargar_archivo(filename, nom_user):
    try:
        buscar = Cipher.objects.get(filename="c2_"+filename)
        var = buscar.filename
        #doc = File(buscar.docfile).read()

    except:
        var = ""
    print var
    print nom_user

    buscar = Cipher.objects.get(filename="c2_"+filename, user_name=nom_user)
    file_c2 = File(buscar.docfile).read()
    #file_c2 = str(open("Cifrados/"+nom_user+"/c2_"+filename+".aes","rb").read())
    #print str(file_c2)
    #hc1 = hashlib.sha256(file_c2).hexdigest()[:16]

    hc = Cipher.objects.get(filename="c2_"+filename,user_name=nom_user)
    doc = hc.hash_c
    print doc
    #buscar = Cipher.objects.all()[:5]
    buscar = Cipher.objects.filter(hash_c=doc).all()[0]
    #buscar.all()[:1]
    #buscar = Cipher.objects.filter(hash_c=doc)
    #print buscar.docfile
    #print buscar.filename
    #buscar = Cipher.objects.get(filename=filename)
    file_c1 = File(buscar.docfile).read()
    #file_c1 = str(open("Cifrados/"+nom_user+"/"+filename+".aes","rb").read())
    #print str(file_c1)

    file_d = open("llaves_clientes/key_d_"+nom_user+".PEM", "rb").read()
    #print str(file_d)

    ##Obtenemos la Clave secreta que se genero en el cifrado
    contentK = hashlib.sha256(file_d).hexdigest()[:16]

    ##Obtenemos el cifrado del archivo
    textcifrado = file_c2
    #print textcifrado

    ##Obtenemos el contenido del vector IV
    iv = open("llaves_clientes/vector_c2_"+filename+"_"+nom_user+".txt","rb").read()
    print iv
    #contentK2 = hashlib.sha256(contentK).hexdigest()[:16]
    print contentK
    plaintext = descifrado(contentK, textcifrado, iv)
    outf = open("Descifrados/"+nom_user+"/c2_"+filename+".txt", "wb")
    outf.write(plaintext)
    outf.close()
    print "Mensaje Descifrado c2: "
    #print plaintext

    contentK=""
    textcifrado=""
    iv=""
    contentK2=""
    temp_cifrado=""

    ##Obtenemos la Clave secreta que se genero en el cifrado
    contentK = plaintext

    ##Obtenemos el cifrado del archivo
    textcifrado = file_c1
    #print textcifrado

    ##Obtenemos el contenido del vector IV
    iv = open("llaves_clientes/vector_" + filename + "_" + nom_user + ".txt", "rb").read()
    print iv
    contentK2 = hashlib.sha256(contentK).hexdigest()[:16]
    contentK2 = open("llaves_clientes/key_z_"+filename+"_"+nom_user+".PEM", "rb").read()
    print contentK2
    plaintext = descifrado(contentK2, textcifrado, iv)
    outf = open("Descifrados/" + nom_user + "/" + filename, "wb")
    outf.write(plaintext)
    outf.close()
    print "Mensaje Descifrado c1: "
    #print plaintext


    # Funcion de decifrado
def descifrado(contentK, textcifrado, iv):
    ctr = Crypto.Util.Counter.new(128, initial_value=long(iv, 16))
    cipher = Crypto.Cipher.AES.new(contentK, Crypto.Cipher.AES.MODE_CTR, counter=ctr)
    return cipher.decrypt(textcifrado)
