from django.forms import *
from django.forms.formsets import formset_factory
from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from domain_models import *

#Formulario del usuario
class UserForm(forms.Form):
    email_field = fields.EmailField(label='E-mail')
    password_field = fields.CharField(label='Password', widget=PasswordInput())

#Formulario del schedule
class ScheduleForm(forms.Form):
    locations = Location.locations()
    day = fields.CharField(widget=fields.HiddenInput())
    in_schedule = fields.BooleanField(label='Viaja?', required=False)
    start_location = fields.ChoiceField(label='Salida', choices=locations)
    start_time = fields.TimeField(label='Horario')
    finish_location = fields.ChoiceField(label='Llegada', choices=locations)
    finish_time = fields.TimeField(label='Horario')
    car = fields.BooleanField(label='Ofrece auto?', required=False)
    avalable_seats = fields.IntegerField(label='lugares')

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
            return HttpResponseRedirect('schedule')
        else:
            context = { 'form': filled_form }
            return TemplateResponse(request, 'login.html', context)

'''
#La pantalla cuando me loguie
#Seguramente esto va a ser otra cosa con sentido, pero es solo para probar
class LoggedScreen(View):

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, 'logged.html')
'''

#La pantalla de armado del schedule
class ScheduleScreen(View):

    def get(self, request, *args, **kwargs):
        ScheduleFormset = formset_factory(ScheduleForm, extra=5, max_num=5)
        schedule_formset = ScheduleFormset(initial=[{'day': 'Lunes'}, {'day': 'Martes'}, 
                                                    {'day': 'Miercoles'}, {'day': 'Jueves'},
                                                    {'day': 'Viernes'}, ])
        context = { 'schedule_formset': schedule_formset }
        return TemplateResponse(request, 'schedule.html', context)

    def post(self, request, *args, **kwargs):
        ScheduleFormset = formset_factory(ScheduleForm, extra=5, max_num=5)
        schedule_formset = ScheduleFormset(request.POST)
        context = { 'schedule_formset': schedule_formset }
        return TemplateResponse(request, 'schedule.html', context)