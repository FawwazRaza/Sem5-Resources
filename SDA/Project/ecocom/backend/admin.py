from django.contrib import admin
from .models import Person, Driver, Rider, Route, Rating, Booking

# Register your models here.

admin.site.register(Person)
admin.site.register(Driver)
admin.site.register(Rider)
admin.site.register(Route)
admin.site.register(Rating)
admin.site.register(Booking)