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
    start_location = fields.ChoiceField(label='Salida', choices=locations, required=False)
    start_time = fields.TimeField(label='Horario', required=False)
    finish_location = fields.ChoiceField(label='Llegada', choices=locations, required=False)
    end_time = fields.TimeField(label='Horario', required=False)
    car = fields.BooleanField(label='Ofrece auto?', required=False)
    avalable_seats = fields.IntegerField(label='lugares', required=False)

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
            request.session['user'] = user
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
        if schedule_formset.is_valid():
            planned_trips = []
            for form in schedule_formset.forms:
                if form.cleaned_data['in_schedule'] == True:
                    user = request.session['user']
                    date = Date.create(form.cleaned_data['day'])
                    interval = Interval.create(form.cleaned_data['start_time'], form.cleaned_data['end_time'])
                    route = Route.create(form.cleaned_data['start_location'], form.cleaned_data['finish_location'])
                    planned_trip = PlannedTrip.create(user, date, interval, route)
                    planned_trips.append(planned_trip)
            context = { 'planned_trips': planned_trips }
            return TemplateResponse(request, 'planned_trips.html', context)
        else:
            context = { 'schedule_formset': schedule_formset }
            return TemplateResponse(request, 'schedule.html', context)