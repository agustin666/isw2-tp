from django.forms import *
from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from domain_models import User

#Formulario del usuario
class UserForm(forms.Form):
    email_field = fields.EmailField(label='E-mail')
    password_field = fields.CharField(label='Password', widget=PasswordInput())

#La pantalla de login
class LoginScreen(View):
    
    def get(self, request, *args, **kwargs):
        form = UserForm()
        context = { 'form': form }
        return TemplateResponse(request, 'login.html', context)
    
    def post(self, request, *args, **kwargs):
        filled_form = UserForm(request.POST)
        user_email = filled_form.data['email_field']
        user_password = filled_form.data['password_field']
        user = User.create(user_email, user_password)
        if user.is_registered():
            return HttpResponseRedirect('logged')
        else:
            context = { 'form': filled_form }
            return TemplateResponse(request, 'login.html', context)
        
#La pantalla cuando me loguie
#Seguramente esto va a ser otra cosa con sentido, pero es solo para probar
class LoggedScreen(View):

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, 'logged.html')