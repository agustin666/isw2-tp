#from django.db import models

class PlannedTrip:
	def user
	def date
	def interval
	def route

class PlannedTripAsDriver(Itinerary):
	def disponibility #int

class PlannedTripAsPassenger(Itinerary):

class User:
	def email #string
	def password #string

class Interval:	
	def start_hour
	def end_hour

class Route:
	def start #location
	def finish #location

class Zone:
	def name #string

class Location:
	def name #string
	def zone

class PlannedTripAdministrator:
	def planned_trips

class xxPlannedTripValidator:
	def validators #por ej de distancia

class PlannedTripCoordinator: #el matching maker
	def match(planned_trips)

class Matching:
	def planned_trips

class Place
	def address #String
	def zone #String
	
	def distanceTo(self, anotherPlace):
		return self.