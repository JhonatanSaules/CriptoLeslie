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
from nube.rsagen import *
from criptoleslie import config
from nube.forms import RegistrationForm, LoginForm

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

    # @method_decorator(csrf_protect)
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated():
    #         return HttpResponseRedirect(config.INDEX_REDIRECT_URL)
    #     else:
    #         return super(RegisterView, self).dispatch(request, *args, **kwargs)

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

class SubirView(TemplateView):
    template_name = 'nube/subir.html'
    #main()






