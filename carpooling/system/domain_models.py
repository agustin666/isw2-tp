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