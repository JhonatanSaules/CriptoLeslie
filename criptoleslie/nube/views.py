import user
import os
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, request
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from nube.rsagen import *
from nube.models import Document
from os import walk
from glob import glob
from os import walk
from nube.Cliente import *
from criptoleslie import config
from nube.forms import RegistrationForm, LoginForm, UploadForm

class LoginView(FormView):
    template_name = 'nube/login.html'
    form_class = LoginForm

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        nom_user=""
        nom_user = form.get_user()
        print nom_user
        f_user = open("llaves_clientes/user.txt", "w")
        f_user.write(str(nom_user))
        f_user.close()
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
        path = '/home/jhonatan/PycharmProjects/CriptoLeslie/criptoleslie/Cifrados/'+user.username

        os.mkdir(path)
        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse('register-success')


class RegisterSuccessView(TemplateView):
    template_name = 'nube/succes.html'

class IndexView(TemplateView):
    template_name = 'nube/index.html'

#class ProfileView(TemplateView):

    # def ls(expr='*.*'):
    #     return glob(expr)
    # print(ls('/home/jhonatan/PycharmProjects/CriptoLeslie/criptoleslie/Cifrados/*'))
    # ls('/home/jhonatan/PycharmProjects/CriptoLeslie/criptoleslie/Cifrados/*')
    # template_name = ''

def lista(request):
    nom_user = open("llaves_clientes/user.txt", "r").read()
    path = '/home/jhonatan/PycharmProjects/CriptoLeslie/criptoleslie/Cifrados/'+nom_user
    # Lista vacia para incluir los ficheros
    lstFiles = []

    # Lista con todos los ficheros del directorio:
    lstDir = os.walk(path)  # os.walk()Lista directorios y ficheros

    for root, dirs, files in lstDir:
        for fichero in files:
            (nombreFichero, extension) = os.path.splitext(fichero)
            lstFiles.append(nombreFichero + extension)

    print(lstFiles)
    print ('LISTADO FINALIZADO')
    return render(request, 'nube/profile.html', {'lstFiles': lstFiles})


def upload_file(request):

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(filename=request.POST['filename'], docfile=request.FILES['docfile'])
            newdoc.save(form)
            nom_user = open("llaves_clientes/user.txt", "r").read()
            subir_arch(newdoc.filename,str(nom_user))
            return redirect("profile")
    else:
        form = UploadForm()
    # tambien se puede utilizar render_to_response
    # return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))
    return render(request, 'nube/upload.html', {'form': form})








