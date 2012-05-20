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
        pass

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

class Route(object):

    @classmethod
    def create(cls, aStartLocation, aFinishLocation):
        route = cls()
        route.start = aStartLocation
        route.finish = aFinishLocation
        return route

class Date(object):

    @classmethod
    def create(cls, aDay):
        date = cls()
        date.day = aDay
        return date
    
class PlannedTripAsDriver(PlannedTrip):
    
    def capacity(self):
        return self.capacity
    
class PlannedTripAsPassenger(PlannedTrip):
    
    def capacity(self):
        return 0
    
class PlannedTripCoordinator(object):

    @classmethod
    def create(cls):
        ptc = cls()
        return ptc
    
    def generateMatchings(self, plannedTrips):
        orderedPlannedTrips = sorted(plannedTrips, key=lambda plannedTrip: plannedTrip.capacity())
        matchings = list()
        
        for t1 in orderedPlannedTrips[:]:
            orderedPlannedTrips.remove(t1)
            if(t1.capacity() > 0):
                matching = Matching.create(t1)
                for t2 in reversed(orderedPlannedTrips)[:]:
                    if(t1.matched(t2)):
                        orderedPlannedTrips.remove(t2)
                        matching.add(t2)
                matchings.append(matching)
            
        return matchings  
      
      
    def matched(plannedTrip1, plannedTrip2):
        return (plannedTrip1.route.start == plannedTrip2.route.start)
    
    
class PlannedTripAdministrator(object):
    
    @classmethod
    def create(cls):
        planned_trip_administrator = cls()
        planned_trip_administrator.trip_validator = PlannedTripValidator.create()
        planned_trip_administrator.trip_validator.add(DistanceValidator.create())
        planned_trip_administrator.trip_coordinator = PlannedTripCoordinator.create()
        planned_trip_administrator.plannedTrips = []
        return planned_trip_administrator
 
    
    def addTrip(self, plannedTrip):
        errors = self.trip_validator.validate(plannedTrip)
        if not errors:
            self.plannedTrips.append(plannedTrip)
        return (plannedTrip, errors)
    
    def addTrips(self, plannedTrips):
        trips_with_errors =[]
        for p in plannedTrips:
            trip_with_errors = self.addTrip(p)
            trips_with_errors.append(trip_with_errors)
        
        return trips_with_errors

            
