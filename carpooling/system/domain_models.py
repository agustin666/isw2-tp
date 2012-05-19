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

    @classmethod
    def create(cls, aUser, aDate, anInterval, aRoute):
        planned_trip = cls()
        planned_trip.user = aUser
        planned_trip.date = aDate
        planned_trip.interval = anInterval
        planned_trip.route = aRoute
        return planned_trip

    def capacity(self):
        return self.capacity

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
                matchings.add(matching)
            
        return matchings
