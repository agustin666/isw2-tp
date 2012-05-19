class User(object):
    
    @classmethod
    def create(cls, anEmail, aPassword):
        self = cls()
        self.email = anEmail
        self.password = aPassword
        return self
    
    def is_registered(self):
        valid_email = self.email == "demo@carpooling.com.ar"
        valid_password = self.password == "asdasd"
        return valid_email and valid_password

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

    capacity
    
    @classmethod
    def create(cls, aUser, aDate, anInterval, aRoute):
        planned_trip = cls()
        planned_trip.user = aUser
        planned_trip.date = aDate
        planned_trip.interval = anInterval
        planned_trip.route = aRoute
        return planned_trip
    
    def capacity():
        return capacity
    
class PlannedTripAsDriver(PlannedTrip):
    
    capacity
    
    def capacity():
        return capacity
    
class PlannedTripAsPassenger(PlannedTrip):
    
    def capacity():
        return 0
    
class PlannedTripCoordinator(object):
    
    def generateMatchings(plannedTrips):
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
        
        
        