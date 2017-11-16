from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class LoginForm(AuthenticationForm):

    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Username")}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Password")}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                classes = self.fields[f_name].widget.attrs.get('class', '')
                classes += ' has-error'
                self.fields[f_name].widget.attrs['class'] = classes

class RegistrationForm(forms.Form):

    # name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(
    #     attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Nombre")}))
    # apellido1 = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(
    #     attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Primer Apellido")}))
    # apellido2 = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(
    #     attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Segundo Apellido")}))
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Nombre de usuario")}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'maxlength': 60, 'class': 'form-control', 'placeholder': _("Correo electronico")}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Contrasena")}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Confirma tu contrasena")}))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = self.fields[f_name].widget.attrs.get('class', '')
                    classes += ' has-error'
                    self.fields[f_name].widget.attrs['class'] = classes

    def clean_username(self):
        try:
            user = User.objects.get(
                username__iexact=self.cleaned_data["username"])
        except User.DoesNotExist:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("Account already exists."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("Passwords don't match."))
        return self.cleaned_data



class UploadForm(forms.Form):
    filename = forms.CharField(max_length=100)
    docfile = forms.FileField(
        label='Selecciona un archivo'
    )