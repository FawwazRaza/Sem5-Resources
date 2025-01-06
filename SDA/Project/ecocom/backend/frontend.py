from abc import ABC, abstractmethod
from backend.models import Person, Driver, Rider
from backend.database import DriverDatabase, RiderDatabase

class FrontendInterface(ABC):
    
    @abstractmethod
    def collect_data(self):
        pass
    
    @abstractmethod
    def register_user(self):
        pass


class Driver(FrontendInterface):
    
    def __init__(self, name, email, phone, person_type, car_model, car_license, seats_available, route, schedule):
        self.name = name
        self.email = email
        self.phone = phone
        self.person_type = person_type
        self.car_model = car_model
        self.car_license = car_license
        self.seats_available = seats_available
        self.route = route
        self.schedule = schedule

    def collect_data(self):
        # Collect data here (assumed that it's already collected)
        return {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'person_type': self.person_type,
            'car_model': self.car_model,
            'car_license': self.car_license,
            'seats_available': self.seats_available,
            'route': self.route,
            'schedule': self.schedule
        }
    
    def register_user(self):
        # Call the database interface to register the driver
        driver_db = DriverDatabase()
        driver_db.register_driver(self.collect_data())


class Rider(FrontendInterface):
    
    def __init__(self, username, name, email, phone, person_type, pickup_location):
        self.username = username
        self.name = name
        self.email = email
        self.phone = phone
        self.person_type = person_type
        self.pickup_location = pickup_location

   
    def collect_data(self):
      
        return {
            'username': "abc1",
            'name': "John Doe",  # Placeholder name
            'email': "johnde@example.com",  # Placeholder email
            'phone': "123457890",  # Placeholder phone number
            'person_type': "Rider",  # Placeholder person type
            'pickup_location': "123 Main St, Cityville"  # Placeholder pickup location
        }
    
    def register_user(self):
        # Call the database interface to register the rider
        rider_db = RiderDatabase()
        rider_db.register_rider(self.collect_data())