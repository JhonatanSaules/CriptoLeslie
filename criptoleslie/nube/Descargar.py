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
        buscar = Hashes.objects.get(filename=filename)
        var = buscar.filename
    except:
        var = ""
    print var
    print nom_user

    file_c2 = open("Cifrados/"+nom_user+"/c2_"+filename+".aes","rb").read()
    #print str(file_c2)

    file_c1 = open("Cifrados/"+nom_user+"/"+filename+".aes","rb").read()
    #print str(file_c1)

    file_d = open("llaves_clientes/key_d_"+nom_user+".PEM", "rb").read()
    #print str(file_d)

    ##Obtenemos la Clave secreta que se genero en el cifrado
    contentK = str(file_d)

    ##Obtenemos el cifrado del archivo
    textcifrado = file_c2

    ##Obtenemos el contenido del vector IV
    iv = open("llaves_clientes/vector_c2_"+filename+"_"+nom_user+".txt","rb").read()
    contentK2 = hashlib.sha256(contentK).hexdigest()[:32]
    plaintext = descifrado(contentK2, textcifrado, iv)
    outf = open("Descifrados/"+nom_user+"/c2_"+filename+".txt", "wb")
    outf.write(plaintext)
    outf.close()
    print "Mensaje Descifrado c2: "
    print plaintext

    ##Obtenemos la Clave secreta que se genero en el cifrado
    contentK = plaintext

    ##Obtenemos el cifrado del archivo
    textcifrado = file_c1

    ##Obtenemos el contenido del vector IV
    iv = open("llaves_clientes/vector_" + filename + "_" + nom_user + ".txt", "rb").read()
    contentK2 = hashlib.sha256(contentK).hexdigest()[:32]
    plaintext = descifrado(contentK2, textcifrado, iv)
    outf = open("Descifrados/" + nom_user + "/" + filename+".jpg", "wb")
    outf.write(plaintext)
    outf.close()
    print "Mensaje Descifrado c1: "
    #print plaintext


    # Funcion de decifrado
def descifrado(contentK, textcifrado, iv):
    ctr = Crypto.Util.Counter.new(128, initial_value=long(iv, 16))
    cipher = Crypto.Cipher.AES.new(contentK, Crypto.Cipher.AES.MODE_CTR, counter=ctr)
    return cipher.decrypt(textcifrado)
