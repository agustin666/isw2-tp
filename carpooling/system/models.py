from django.db import models

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
	start #location
	finish #location

class Zone:
	name #string

class Location:
	name #string
	zone

class PlannedTripAdministrator:
	planned_trips

class xxPlannedTripValidator:
	validators #por ej de distancia

class PlannedTripCoordinator: #el matching maker
	def match(planned_trips)

class Matching:
	planned_trips
