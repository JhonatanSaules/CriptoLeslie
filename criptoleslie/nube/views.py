import os
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from nube.models import Document
from nube.Cliente import *
from criptoleslie import config
from nube.forms import RegistrationForm, LoginForm, UploadForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


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

def ValidateEmail(email):
    try:
        validate_email(email)
        print True
        return True
    except ValidationError:
        print False
        return False

def verificar_clave(passw):

    if not 6 <= len(passw) <= 12:
        is_valid2 = 0
        return 0

    numeros = 0
    mayusculas = 0
    minusculas = 0

    for carac in passw:
        if carac.isspace():
            return False
        elif carac.isdigit():
            numeros += 1
        elif carac.isupper():
            mayusculas += 1
        elif carac.islower():
            minusculas += 1
    if numeros >= 4 and mayusculas !=0 and minusculas >= 4:
        is_valid2 = 1
        return 1

class RegisterView(FormView):
    template_name = 'nube/register.html'
    form_class = RegistrationForm
    def form_valid(self, form):

        verificar_clave(form.cleaned_data['password1'])
        is_valid = ValidateEmail(form.cleaned_data['email'])
        if is_valid:
            print("El email es correcto")
            user = User.objects.create_user(
                #firstname=form.cleaned_data["firstname"],
                #lastname=form.cleaned_data["lastname"],
                # apellido2=form.cleaned_data["apellido2"],
                username=form.cleaned_data["username"],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            # print (validate_email(user.email))
            # is_valid = validate_email(user.email)
            # print is_valid
            gen_rsa(user.username)
            path = '/home/jhonatan/PycharmProjects/CriptoLeslie/criptoleslie/Cifrados/' + user.username
            os.mkdir(path)
            path2 = '/home/jhonatan/PycharmProjects/CriptoLeslie/criptoleslie/hash/' + user.username
            os.mkdir(path2)
            return super(RegisterView, self).form_valid(form)
        else:
            print("El email es incorrecto")

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
            print newdoc.docfile.name
            nom_user = open("llaves_clientes/user.txt", "r").read()
            subir_arch(newdoc.filename,str(nom_user))
            return redirect("profile")
    else:
        form = UploadForm()
    # tambien se puede utilizar render_to_response
    # return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))
    return render(request, 'nube/upload.html', {'form': form})



#class DownloadView(TemplateView):
 #   template_name = 'nube/download.html'

def download(request):
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

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(filename=request.POST['filename'], docfile=request.FILES['docfile'])
            newdoc.save(form)
            print newdoc.docfile.name
            nom_user = open("llaves_clientes/user.txt", "r").read()
            subir_arch(newdoc.filename,str(nom_user))
            return redirect("profile")
    else:
        form = UploadForm()

    return render(request, 'nube/download.html', {'lstFiles': lstFiles})







