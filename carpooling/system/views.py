#coding=UTF-8

from django.forms import *
from django.forms.formsets import formset_factory
from django.views.generic import View
from django.template.response import TemplateResponse
from django.shortcuts import redirect

from domain_models import *

locations = Locations.create()

#Para tener algo de persistencia
class ObjectCollectionSaver(object):
    
    @classmethod
    def load(cls, request, name):
        pts = cls()
        pts.session = request.session
        if not name in pts.session:
            pts.session[name] = []
        pts.objects = pts.session[name]
        return pts
    
    def add(self, object):
        self.objects.append(object)
        self.session.modified = True
        return
    
    def add_many(self, objects):
        self.objects += objects
        self.session.modified = True
        return

    def clear(self):
        del self.objects[:]
        self.session.modified = True
        return
    
    def get_all(self):
        return self.objects

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

    def clean(self):
        cleaned_data = super(ScheduleForm, self).clean()
        in_schedule = cleaned_data.get("in_schedule")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if in_schedule and (not start_time or not end_time):
            raise forms.ValidationError("Debe especificar un horario de salida y llegada.")
        return cleaned_data

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
            saver = ObjectCollectionSaver.load(request, 'users')
            saver.add(user)
            return redirect('login')
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
            saver = ObjectCollectionSaver.load(request, 'users')
            users = Users.create(saver.get_all())
            if users.passwordOk(user_email, user_password):
                request.session['user'] = users.get_user(user_email)
                return redirect('schedule')
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
                    avalable_seats = form.cleaned_data['avalable_seats']
                    if form.cleaned_data['car']:
                        planned_trip = PlannedTripAsDriver.create(user, date, interval, route, avalable_seats)
                    else:
                        planned_trip = PlannedTripAsPassenger.create(user, date, interval, route)
                    planned_trips.append(planned_trip)
            planned_trip_admin = PlannedTripAdministrator.create()
            trips_with_errors = planned_trip_admin.addTrips(planned_trips)
            saver = ObjectCollectionSaver.load(request, 'planned_trips')
            saver.add_many(planned_trip_admin.planned_trips)
            return TemplateResponse(request, 'planned_trips.html', 
                                    { 'trips_with_errors': trips_with_errors })
        else:
            context = { 'schedule_formset': schedule_formset }
            return TemplateResponse(request, 'schedule.html', context)
        
class SavedPlannedTripsScreen(View):
    
    def get(self, request, *args, **kwargs):
        saver = ObjectCollectionSaver.load(request, 'planned_trips')
        spt = saver.get_all()
        return TemplateResponse(request, 'saved_planned_trips.html', 
                                {'spt': spt})

class DeletePlannedTrips(View):
    
    def get(self, request, *args, **kwargs):
        saver = ObjectCollectionSaver.load(request, 'planned_trips')
        saver.clear()
        return redirect('saved_planned_trips')
    
class MatchingScreen(View):
    
    def get(self, request,*args, **kwargs):
        saver = ObjectCollectionSaver.load(request, 'planned_trips')
        planned_trips = saver.get_all()
        planned_trip_admin = PlannedTripAdministrator.create()
        matchings = planned_trip_admin.generateMatchings(planned_trip_admin.plannedTrips())
        context = { 'matchings': matchings }
        
        return TemplateResponse(request, 'matchings.html', context) 

class DeleteUsers(View):
    
    def get(self, request, *args, **kwargs):
        saver = ObjectCollectionSaver.load(request, 'users')
        saver.clear()
        return redirect('users')

class UsersScreen(View):
    
    def get(self, request, *args, **kwargs):
        saver = ObjectCollectionSaver.load(request, 'users')
        users = saver.get_all()
        return TemplateResponse(request, 'users.html', 
                                {'users': users})
