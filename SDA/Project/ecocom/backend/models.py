from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Custom Person model
class Person(models.Model):
    PERSON_TYPE_CHOICES = [
        ('Driver', 'Driver'),
        ('Rider', 'Rider'),
    ]

    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='Username must be alphanumeric'
            )
        ]
    )
    password = models.CharField(max_length=128)  # Store hashed password
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^03\d{9}$',
                message='Phone number must start with 03 and be 11 digits'
            )
        ]
    )
    person_type = models.CharField(max_length=10, choices=PERSON_TYPE_CHOICES)

    def clean(self):
        # Ensure unique constraints for username, email, and phone
        if Person.objects.filter(username=self.username).exclude(pk=self.pk).exists():
            raise ValidationError("Username already exists")
        if Person.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError("Email already exists")
        if Person.objects.filter(phone=self.phone).exclude(pk=self.pk).exists():
            raise ValidationError("Phone number already exists")

    def save(self, *args, **kwargs):
        # Hash the password before saving
        
        self.clean()  # Ensure validation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.person_type})"


# Driver model
class Driver(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="driver_profile")
    car_model = models.CharField(max_length=100)
    car_license = models.CharField(max_length=50)
    seats_available = models.PositiveIntegerField()
    route = models.JSONField(default=list)  # A list of locations
    timing = models.CharField(max_length=20, default="")  # String value for schedule

    def __str__(self):
        return f"Driver: {self.person.name}"


# Rider model
class Rider(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="rider_profile")
    pickup_location = models.CharField(max_length=255)

    def __str__(self):
        return f"Rider: {self.person.name}"


# Rating model
class Rating(models.Model):
    from_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="given_ratings")
    to_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="received_ratings")
    score = models.PositiveSmallIntegerField()  # Between 1 and 5
    feedback = models.TextField(max_length=500)

    def __str__(self):
        return f"Rating: {self.score} from {self.from_person.name} to {self.to_person.name}"


# Booking model
class Booking(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="bookings")
    riders = models.ManyToManyField(Rider, related_name="bookings")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.driver.person.name} with {self.riders.count()} riders"


# Route model
class Route(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, related_name="driver_route")
    locations = models.JSONField()  # Stores a list of up to 10 locations as JSON.

    def __str__(self):
        return f"Route for {self.driver.person.name}"
