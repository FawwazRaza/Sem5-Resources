"""
URL configuration for eco project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from backend.views import (
    login_view, 
    register_view, 
    search_rides, 
    book_ride, 
    rider_profile_view, 
    rider_bookings_view,  
    logout_view,
    driver_profile_view,
    driver_bookings_view,
    update_driver_profile_view,
    driver_cancel_booking_view,
    driver_rate_rider_view,
    rider_cancel_booking_view,
    rider_location_view,
    rider_rating_view,
    search_rides_view
)
from backend.database import DriverDatabase, RiderDatabase 
urlpatterns = [
    # Admin path
    path('admin/', admin.site.urls),

    # API paths
    path('api/login/', login_view, name='login'),
    path('api/register/', register_view, name='register'),
    path('api/search-rides/', search_rides, name='search_rides'),
    path('api/book-ride/', book_ride, name='book_ride'),
    path('api/rider/profile/', rider_profile_view, name='rider_profile'),
    # path('api/cancel-booking/', cancel_booking_view, name='cancel_booking'),
    path('api/logout/', logout_view, name='logout'),

    # Template paths for static pages
    path('', TemplateView.as_view(template_name='index.html')),
    path('login/', TemplateView.as_view(template_name='login.html')),
    path('register/', TemplateView.as_view(template_name='register.html')),
    path('driver/dashboard/', TemplateView.as_view(template_name='driver-dashboard.html')),
    path('rider/dashboard/', TemplateView.as_view(template_name='rider-dashboard.html')),

    path('api/rider/search-rides/', search_rides_view, name='search_rides'),

  # Driver Dashboard Paths
    path('driver/dashboard/', TemplateView.as_view(template_name='driver-dashboard.html'), name='driver_dashboard'),
    
    # API Endpoints for Driver Database Methods
    path('api/driver/profile/',        driver_profile_view, name='driver_profile'),
    path('api/driver/bookings/',       driver_bookings_view, name='driver_bookings'),
    # path('api/driver/cancel-booking/', cancel_booking_view, name='cancel_booking'),
    path('api/driver/update-profile/', update_driver_profile_view, name='update_driver_profile'),

    path('api/driver/cancel-booking/', driver_cancel_booking_view, name='driver_cancel_booking'),
    path('api/driver/rate-rider/', driver_rate_rider_view, name='driver_rate_rider'),
    
    # Rider Booking URLs
    path('api/rider/bookings/', rider_bookings_view, name='rider_bookings'),
    path('api/rider/cancel-booking/', rider_cancel_booking_view, name='rider_cancel_booking'),
    path('api/rider/location/', rider_location_view, name='rider_location'),
    path('api/rider/rating/', rider_rating_view, name='rider_rating'),
]

