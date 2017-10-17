from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, request
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from Crypto.PublicKey import RSA
from criptoleslie import config
from nube.forms import RegistrationForm, LoginForm

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
    # type: (object) -> object
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

class LoginView(FormView):
    template_name = 'nube/login.html'
    form_class = LoginForm

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        try:
            return config.LOGIN_REDIRECT_URL
        except:
            return "/profile/"


class LogoutView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LogoutView, self).dispatch(*args, **kwargs)

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(config.LOGOUT_REDIRECT_URL)


class RegisterView(FormView):
    template_name = 'nube/register.html'
    form_class = RegistrationForm

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(config.INDEX_REDIRECT_URL)
        else:
            return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        user = User.objects.create_user(
            # name=form.cleaned_data["name"],
            # apellido1=form.cleaned_data["apellido1"],
            # apellido2=form.cleaned_data["apellido2"],
            username=form.cleaned_data["username"],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
        )
        gen_rsa(user.username)

        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse('register-success')


class RegisterSuccessView(TemplateView):
    template_name = 'nube/succes.html'

class IndexView(TemplateView):
    template_name = 'nube/index.html'

class ProfileView(TemplateView):
    template_name = 'nube/profile.html'





