#coding=UTF-8

from django.forms import *
from django.forms.formsets import formset_factory
from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from domain_models import *

locations = Locations.create()

#Formulario del usuario
class UserForm(forms.Form):
    email_field = fields.EmailField(label='E-mail')
    password_field = fields.CharField(label='Password', widget=PasswordInput())

#Formulario del schedule
location_choices = [(location.name, location) for location in locations.get_all()]
class ScheduleForm(forms.Form):
    day = fields.CharField(widget=fields.HiddenInput())
    in_schedule = fields.BooleanField(label='Viaja?', required=False)
    start_location = fields.ChoiceField(label='Salida', choices=location_choices, required=False)
    start_time = fields.TimeField(label='Horario', required=False)
    finish_location = fields.ChoiceField(label='Llegada', choices=location_choices, required=False)
    end_time = fields.TimeField(label='Horario', required=False)
    car = fields.BooleanField(label='Ofrece auto?', required=False)
    avalable_seats = fields.IntegerField(label='Lugares', required=False)

class UserRegistrationForm(forms.Form):
    user_name_field = fields.CharField(label='Nombre')
    email_field = fields.EmailField(label='E-mail')
    password_field = fields.CharField(label='Password', widget=PasswordInput())

class RegistrationScreen(View):

    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        context = { 'form': form }
        return TemplateResponse(request, 'registration.html', context)
    
    def post(self, request, *args, **kwargs):
        filled_form = UserRegistrationForm(request.POST)
        if filled_form.is_valid():
            user_name = filled_form.cleaned_data['user_name_field']
            user_email = filled_form.cleaned_data['email_field']
            user_password = filled_form.cleaned_data['password_field']
            user = User.create(user_name, user_email, user_password)
            return HttpResponseRedirect('login')
        else:
            context = { 'form': filled_form }
            return TemplateResponse(request, 'registration.html', context)

#La pantalla de login
class LoginScreen(View):
    
    def get(self, request, *args, **kwargs):
        form = UserForm()
        context = { 'form': form }
        return TemplateResponse(request, 'login.html', context)
    
    def post(self, request, *args, **kwargs):
        filled_form = UserForm(request.POST)
        error_message = None
        if filled_form.is_valid():
            user_email = filled_form.data['email_field']
            user_password = filled_form.data['password_field']
            users = Users.create()
            if users.passwordOk(user_email, user_password):
                request.session['user'] = users.get_user(user_email)
                return HttpResponseRedirect('schedule')
            else:
                error_message = 'El usuario y/o contraseña ingresados son invalidos'
        context = { 'form': filled_form, 'error_message': error_message }
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
                if form.cleaned_data['in_schedule']:
                    user = request.session['user']
                    date = Date.create(form.cleaned_data['day'])
                    interval = Interval.create(form.cleaned_data['start_time'], form.cleaned_data['end_time'])
                    start_location = locations.find_by_name(form.cleaned_data['start_location'])
                    finish_location = locations.find_by_name(form.cleaned_data['finish_location'])
                    route = Route.create(start_location, finish_location)
                    if form.cleaned_data['car']:
                        planned_trip = PlannedTripAsDriver.create(user, date, interval, route)
                    else:
                        planned_trip = PlannedTripAsPassenger.create(user, date, interval, route)
                    planned_trips.append(planned_trip)
            planned_trip_admin = PlannedTripAdministrator.create()
            trips_with_errors = planned_trip_admin.addTrips(planned_trips)
            return TemplateResponse(request, 'planned_trips.html', 
                                    { 'trips_with_errors': trips_with_errors })
        else:
            context = { 'schedule_formset': schedule_formset }
            return TemplateResponse(request, 'schedule.html', context)
        
class AdministrateScreen(View):
    
    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, 'administrate.html')
    
class MatchingScreen(View):
    
    def get(self, request,*args, **kwargs):
        administrator = PlannedTripAdministrator.create()
        matchings = administrator.generateMatchings()
        context = { 'matchings': matchings }
        
        return TemplateResponse(request, 'matchings.html', context) 
