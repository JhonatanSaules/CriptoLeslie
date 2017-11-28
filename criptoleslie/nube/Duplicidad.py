from django.core.files import File
from models import Hashes,Cipher

def deduplication(hc1,nom_user,filename2,fc1,fc2):
    print "Checando duplicidad"
    hc=""
    var=""
    try:
        hc = Hashes.objects.get(hash_c=hc1)
        var = hc.hash_c
        doc = File(hc.docfile).read()

        print doc
    except:
        var = ""
    #hash_comp = open("hash/"+nom_user+"/"+str(var)+".sha", "rb").read()
    ##hash_comp = ""
    #print str(hash_comp)
    print var
    print hc
    print hc1
    if str(var) == hc1:
        print "Duplicado detectado"
        filec2= open("Cifrados/"+nom_user+"/c2_"+filename2+".aes","wb")
        filec2.write(str(fc2))
        filec2.close()
        f = open("Cifrados/"+nom_user+"/c2_"+filename2+".aes")
        f.read()
        try:
            Cipher.objects.get(filename="c2_"+filename2,user_name=nom_user)
            cont=1
            print "try: "+str(cont)
        except:
            cont=0
            print "except: "+str(cont)

        if cont==0:
            newdoc = Cipher(filename="c2_"+filename2, hash_c=hc1, user_name=nom_user, docfile=File(f))
            newdoc.save(File(f))
            f.close()
        else:
            print "nada"

    else:
        print "Archivo nuevo"
        hash_c1 = open("hash/"+nom_user+"/"+filename2+".sha","wb")
        hash_c1.write(str(hc1))
        hash_c1.close()
        f = open("hash/"+nom_user+"/"+filename2+".sha")
        f.read()
        print str(f)
        newdoc = Hashes(filename=filename2,hash_c=hc1, docfile=File(f))
        newdoc.save(File(f))
        f.close()
        filec1 = open("Cifrados/"+nom_user+"/"+filename2+".aes","wb")
        filec1.write(str(fc1))
        filec1.close()
        f = open("Cifrados/"+nom_user+"/"+filename2+".aes")
        f.read()
        newdoc = Cipher(filename=filename2, hash_c=hc1, user_name=nom_user, docfile=File(f))
        newdoc.save(File(f))
        f.close()
        filec2 = open("Cifrados/"+nom_user+"/c2_"+filename2+".aes", "wb")
        filec2.write(str(fc2))
        filec2.close()
        f = open("Cifrados/"+nom_user+"/c2_"+filename2+".aes")
        f.read()
        newdoc = Cipher(filename="c2_"+filename2, hash_c=hc1, user_name=nom_user, docfile=File(f))
        newdoc.save(File(f))
        f.close()




