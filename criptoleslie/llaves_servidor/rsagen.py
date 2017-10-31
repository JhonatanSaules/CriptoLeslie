from Crypto.PublicKey import RSA
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q,r = b//a,b%a; m,n = x-u*q,y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    return b, x, y

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

def inv_mult(a,n):
 if(egcd(a,n)!=1):
  print(str(a) + " NO TIENE INVERSO MULTIPLICATIVO EN " + str(n))
 else:
  for i in range(1,n) :
   if( ( a*i-1 )%n == 0 ):
    return i


def gen_rsa(usuario):
    e1 = 60930653384725765076332500645556642152211806415934766914695520823273026175616848699473936010624731806269142093271913689159213872865076416589044315502632688917901661349440933320674987852270733473960723266314414642607492951577749038396798784104542574870595087423906384652288903187482471046260836989527934228913249366654703107866541602432023727251827
    RSAkey = RSA.generate(1024)
    phi = (RSAkey.p -1)*(RSAkey.q-1)
    #print ('p:', RSAkey.p)
    #print ('q:', RSAkey.q)
    #print ('n:', RSAkey.n)
    #print ('phi:', phi)
    e = e1 % phi
    #print ('e:', e)
    d = modinv(e,phi)
    #print ('d:', d)
    #x = 2342424223478
    #y = pow(x,e1, RSAkey.n)
    #z = pow(y,d, RSAkey.n)
    #if x ==z:
    #   print "Funciona"
    #else:
    #   print "Murio"
    nom = ''
    nom = str(usuario)
    f_n = open("key_n_"+nom+".PEM", "w")
    f_e = open("key_e_"+nom+".PEM", "w")
    f_d = open("key_d_"+nom+".PEM", "w")
    f_n.write(str(RSAkey.n))
    f_n.close()
    f_d.write(str(d))
    f_d.close()
    f_e.write(str(e))
    f_e.close()

