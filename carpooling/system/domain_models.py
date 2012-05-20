from abc import ABCMeta, abstractmethod

class Users(object):
    
    @classmethod
    def create(cls):
        users = cls()
        user1 = User.create('David Trezeguet', 'demo@carpooling.com.ar', 'asdasd')
        users.list = [user1, ]
        return users
    
    def user_is_registered(self, anEmail, aPassword):
        for user in self.list:
            if user.email == anEmail and user.password == aPassword:
                return True
        return False

    def get_user_with(self, anEmail, aPassword):
        for user in self.list:
            if user.email == anEmail and user.password == aPassword:
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

class Location(object):

    @classmethod
    def create(cls, aName, aZone):
        location = cls()
        location.name = aName
        location.zone = aZone
        return location

    @classmethod
    def locations(cls):
        tigre = Zone.create('Tigre')
        capfed = Zone.create('Capital Federal')
        belgrano = cls.create('Belgrano', capfed)
        monserrat = cls.create('Monserrat', capfed)
        torcuato = cls.create('Don Torcuato', tigre)
        return ((belgrano.name, belgrano), (torcuato.name, torcuato), (monserrat.name, monserrat))
    
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
        validation_results = []
        for validator in self.validators:
            validation_results.append(validator.validate(aPlannedTrip))
        return validation_results

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
        if aPlannedtrip.route.start != aPlannedtrip.route.finish:
            return ValidationResult.create(aPlannedtrip, "OK")
        else:
            return ValidationResult.create(aPlannedtrip, "ERROR")
    
class ValidationResult(object):

    @classmethod
    def create(cls, aSubject, aMessage):
        validation_result = cls()
        validation_result.subject = aSubject
        validation_result.message = aMessage
        return validation_result

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
        return errors
    
    def addTrips(self, plannedTrips):
        dict_errors = {}
        for p in plannedTrips:
            errors = self.addTrip(p)
            if not errors:
                dict_errors[p.date] = errors
        
        return dict_errors

            
