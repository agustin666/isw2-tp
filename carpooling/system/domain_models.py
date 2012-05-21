from django.utils.datetime_safe import datetime
from abc import ABCMeta, abstractmethod

class Users(object):
    
    @classmethod
    def create(cls):
        users = cls()
        user1 = User.create('David Trezeguet', 'demo@carpooling.com.ar', 'asdasd')
        users.list = [user1, ]
        return users
    
    def passwordOk(self, anEmail, aPassword):
        user = self.get_user(anEmail)
        return user and user.password == aPassword

    def get_user(self, anEmail):
        for user in self.list:
            if user.email == anEmail:
                return user
        return None

class User(object):
    
    @classmethod
    def create(cls, aName, anEmail, aPassword):
        user = cls()
        user.name = aName
        user.email = anEmail
        user.password = aPassword
        return user

class Zone(object):

    @classmethod
    def create(cls, aName):
        zone = cls()
        zone.name = aName
        return zone

    def __unicode__(self):
        return self.name

class Locations(object):
    
    @classmethod
    def create(cls):
        tigre = Zone.create('Tigre')
        capfed = Zone.create('Capital Federal')
        belgrano = Location.create('Belgrano', capfed)
        monserrat = Location.create('Monserrat', capfed)
        torcuato = Location.create('Don Torcuato', tigre)
        locations = cls()
        locations.list = [belgrano, monserrat, torcuato]
        return locations
    
    def get_all(self):
        return self.list
    
    def find_by_name(self, locationName):
        for location in self.list:
            if location.name == locationName:
                return location
        return None

class Location(object):

    @classmethod
    def create(cls, aName, aZone):
        location = cls()
        location.name = aName
        location.zone = aZone
        return location

        #return ((belgrano.name, belgrano), (torcuato.name, torcuato), (monserrat.name, monserrat))
    
    def __unicode__(self):
        return '%s, %s' % (self.name, self.zone.name)

class PlannedTrip(object):
    __metaclass__ = ABCMeta

    @classmethod
    def create(cls, aUser, aDate, anInterval, aRoute):
        planned_trip = cls()
        planned_trip.user = aUser
        planned_trip.date = aDate
        planned_trip.interval = anInterval
        planned_trip.route = aRoute
        return planned_trip

    @abstractmethod
    def capacity(self):
        return

class PlannedTripValidator(object):
 
    @classmethod
    def create(cls):
        ptv = cls()
        ptv.validators = []
        return ptv
    
    def add(self, validator):
        self.validators.append(validator)
        return
    
    def validate(self, aPlannedTrip):
        validation_errors = []
        for validator in self.validators:
            result = validator.validate(aPlannedTrip)
            if result.is_error():
                validation_errors.append(result)
        return validation_errors

class Validator(object):
    __metaclass__ = ABCMeta

    @classmethod
    def create(cls):
        validator = cls()
        return validator

    @abstractmethod
    def validate(self, aPlannedtrip):
        return

class DistanceValidator(Validator):

    def validate(self, aPlannedtrip):
        if aPlannedtrip.route.start.zone != aPlannedtrip.route.finish.zone:
            return ValidationResult.create(aPlannedtrip, "OK")
        else:
            return ValidationResult.create(aPlannedtrip, "ERROR", 
                                           "El viaje debe ser de 20km o mas " + 
                                           "de distancia")
    
class ValidationResult(object):

    @classmethod
    def create(cls, aSubject, aType, aMessage=''):
        validation_result = cls()
        validation_result.subject = aSubject
        validation_result.type = aType
        validation_result.message = aMessage
        return validation_result
    
    def is_error(self):
        return self.type == "ERROR"


class Interval(object):

    @classmethod
    def create(cls, aStartHour, anEndHour):
        interval = cls()
        interval.start_hour = aStartHour
        interval.end_hour = anEndHour
        return interval
    
    def __eq__(self, other):
        return self.start_hour == other.start_hour and self.end_hour == other.end_hour

class Route(object):

    @classmethod
    def create(cls, aStartLocation, aFinishLocation):
        route = cls()
        route.start = aStartLocation
        route.finish = aFinishLocation
        return route
    
    def __eq__(self, other):
        return self.start == other.start and self.finish == other.finish

class Date(object):

    @classmethod
    def create(cls, aDay):
        date = cls()
        date.day = aDay
        return date
    
class PlannedTripAsDriver(PlannedTrip):

    @classmethod
    def create(cls, aUser, aDate, anInterval, aRoute, aCapacity):
        planned_trip_as_driver = super(PlannedTripAsDriver,cls).create(aUser, aDate, anInterval, aRoute)
        planned_trip_as_driver.capacity = aCapacity
        return planned_trip_as_driver
    
    def capacity(self):
        return self.capacity
    
class PlannedTripAsPassenger(PlannedTrip):
    
    @classmethod
    def create(cls, aUser, aDate, anInterval, aRoute):
        planned_trip_as_driver = super(PlannedTripAsPassenger,cls).create(aUser, aDate, anInterval, aRoute)
        planned_trip_as_driver.capacity = 0
        return planned_trip_as_driver
    
    def capacity(self):
        return self.capacity
    
class PlannedTripCoordinator(object):
    
    @classmethod
    def create(cls):
        planned_trip_coordinator = cls()
        return planned_trip_coordinator
    
    def generateMatchings(self, planned_trips):
        ordered_planned_trips = sorted(planned_trips, key=lambda p: p.capacity).reverse()
        matchings = []
        
        for t1 in ordered_planned_trips[:]:
            ordered_planned_trips.remove(t1)
            if(t1.capacity() > 0):
                matching = Matching.create(t1)
                for t2 in reversed(ordered_planned_trips)[:]:
                    if(matching.full()):
                        break
                    if(t1.matched(t2)):
                        ordered_planned_trips.remove(t2)
                        matching.add(t2)
                matchings.append(matching)
            
        return matchings  
      
      
    def matched(plannedTrip1, plannedTrip2):
        return plannedTrip1.route == plannedTrip2.route and plannedTrip1.interval == plannedTrip2.interval
    
    
class PlannedTripAdministrator(object):
    
    @classmethod
    def create(cls):
        planned_trip_administrator = cls()
        planned_trip_administrator.trip_validator = PlannedTripValidator.create()
        planned_trip_administrator.trip_validator.add(DistanceValidator.create())
        planned_trip_administrator.trip_coordinator = PlannedTripCoordinator.create()
        planned_trip_administrator.planned_trips = []
        return planned_trip_administrator
 
    
    def addTrip(self, plannedTrip):
        errors = self.trip_validator.validate(plannedTrip)
        if not errors:
            self.planned_trips.append(planned_trip)
        return errors
    
    def addTrips(self, planned_trips):
        dict_errors = {}
        for p in planned_trips:
            errors = self.add_trip(p)
            if not errors:
                dict_errors[p.date] = errors
        
        return dict_errors
    
    def generateMatchings(self):
        self.trip_coordinator.generateMatchings(self.plannedTrips())
        
    def plannedTrips(self):
        
        planned_trips = []
        
        user1 = User.create("Miguel", "miguel@gmail.com", "facil")
        user2 = User.create("Agustin", "agustin@gmail.com", "facil")
        user3 = User.create("Luciano", "luciano@gmail.com", "facil")
        user4 = User.create("Lucas", "lucas@gmail.com", "facil")
        
        date1 = Date.create("Lunes")
        
        anInterval = Interval.create(datetime.strptime('10:00',"%H:%M"), datetime.strptime('18:00',"%H:%M"))
        
        salida = Location.create('Monserrat', Zone.create("Capital Federal"))
        llegada = Location.create('Torcuato', Zone.create("Tigre"))
        aRoute = Route.create(salida, llegada)
        
        p1 = PlannedTripAsDriver.create(user1, date1, anInterval, aRoute, 3)
        p2 = PlannedTripAsPassenger.create(user2, date1, anInterval, aRoute)
        p3 = PlannedTripAsPassenger.create(user3, date1, anInterval, aRoute)
        p4 = PlannedTripAsPassenger.create(user4, date1, anInterval, aRoute)
        
        planned_trips.append(p1)
        planned_trips.append(p2)
        planned_trips.append(p3)
        planned_trips.append(p4)
        
        return planned_trips

class Matching(object):
    
    @classmethod
    def create(cls, owner):
        matching = cls()
        matching.owner = owner
        matching.trips = []
        matching.free_places = owner.capacity()
        
    def add(self, planned_trip):
        self.trips.append(planned_trip)
        self.free_places = self.free_places - 1 
        
    def full(self):
        return self.free_places == 0