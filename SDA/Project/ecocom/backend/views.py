import json
import logging
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_protect
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.contrib.auth import logout
from .models import Person, Rider, Driver, Booking, Rating
from .database import DriverDatabase, RiderDatabase

from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone
from datetime import timedelta


# Setup logger
logger = logging.getLogger(__name__)

@csrf_protect
@require_http_methods(["POST"])
@csrf_protect
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user_type = data.get('user_type')

        # Validate input
        if not all([username, password, user_type]):
            return JsonResponse({
                'success': False, 
                'message': 'Missing username, password, or user type'
            })

        # Choose appropriate database interface based on user type
        if user_type == 'Driver':
            db = DriverDatabase()
        else:
            db = RiderDatabase()

        # Set person_type for authentication
        db.person_type = user_type

        # Authenticate user
        if db.authenticateLogin(username, password):
            # Create session or token (simplified for this example)
            request.session['username'] = username
            request.session['user_type'] = user_type
            
            return JsonResponse({
                'success': True, 
                'message': 'Login successful',
                'user_type': user_type
            })
        else:
            return JsonResponse({
                'success': False, 
                'message': 'Invalid credentials'
            })
    except Exception as e:
        print(f"Login error: {e}")
        return JsonResponse({
            'success': False, 
            'message': f'Unexpected error: {str(e)}'
        })
    
@csrf_protect
@require_http_methods(["POST"])
def logout_view(request):
    try:
        # Django logout
        logout(request)
        
        # Clear session
        request.session.flush()
        
        return JsonResponse({
            'success': True, 
            'message': 'Logged out successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': str(e)
        })
    
# @csrf_protect
# def register_view(request):
#     if request.method == 'POST':
#         try:
#             # Parse the JSON data from the request body
#             data = json.loads(request.body)
            
#             # Validate required fields
#             required_fields = ['username', 'name', 'email', 'phone', 'password', 'person_type']
#             for field in required_fields:
#                 if field not in data:
#                     return JsonResponse({
#                         'success': False, 
#                         'message': f'Missing required field: {field}'
#                     }, status=400)
            
#             # Create Person object
#             person = Person(
#                 username=data['username'],
#                 name=data['name'],
#                 email=data['email'],
#                 phone=data['phone'],
#                 password=data['password'],
#                 person_type=data['person_type']
#             )
            
#             # Validate and save Person
#             person.full_clean()
#             person.save()
            
#             # Create additional profile based on person type
#             if data['person_type'] == 'Driver':
#                 # Validate driver-specific fields
#                 driver_fields = ['car_model', 'car_license', 'seats_available']
#                 for field in driver_fields:
#                     if field not in data:
#                         # Rollback person creation if driver fields are missing
#                         person.delete()
#                         return JsonResponse({
#                             'success': False, 
#                             'message': f'Missing driver field: {field}'
#                         }, status=400)
                
#                 # Create Driver profile
#                 driver = Driver(
#                     person=person,
#                     car_model=data['car_model'],
#                     car_license=data['car_license'],
#                     seats_available=data['seats_available'],
#                     route=data.get('route', []),
#                     timing=data.get('timing', '')
#                 )
#                 driver.save()
            
#             elif data['person_type'] == 'Rider':
#                 # Create Rider profile
#                 rider = Rider(
#                     person=person,
#                     pickup_location=data.get('pickup_location', '')
#                 )
#                 rider.save()
            
#             return JsonResponse({
#                 'success': True, 
#                 'message': 'Registration successful'
#             })
        
#         except Exception as e:
#             # Comprehensive error handling
#             return JsonResponse({
#                 'success': False, 
#                 'message': str(e)
#             }, status=500)
    
#     # Handle non-POST requests
#     return JsonResponse({
#         'success': False, 
#         'message': 'Invalid request method'
#     }, status=405)
@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['username', 'name', 'email', 'phone', 'password', 'person_type']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        'success': False, 
                        'message': f'Missing required field: {field}'
                    }, status=400)
            
            # Create Person object
            person = Person(
                username=data['username'],
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                password=data['password'],
                person_type=data['person_type']
            )
            
            # Validate and save Person
            person.full_clean()
            person.save()
            
            # Create additional profile based on person type
            if data['person_type'] == 'Driver':
                # Validate driver-specific fields
                driver_fields = ['car_model', 'car_license', 'seats_available']
                for field in driver_fields:
                    if field not in data:
                        # Rollback person creation if driver fields are missing
                        person.delete()
                        return JsonResponse({
                            'success': False, 
                            'message': f'Missing driver field: {field}'
                        }, status=400)
                
                # Create Driver profile
                driver = Driver(
                    person=person,
                    car_model=data['car_model'],
                    car_license=data['car_license'],
                    seats_available=data['seats_available'],
                    route=data.get('route', []),
                    timing=data.get('timing', '')
                )
                driver.save()
            
            elif data['person_type'] == 'Rider':
                # Create Rider profile
                rider = Rider(
                    person=person,
                    pickup_location=data.get('pickup_location', '')
                )
                rider.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'Registration successful'
            })
        
        except Exception as e:
            # Comprehensive error handling
            return JsonResponse({
                'success': False, 
                'message': str(e)
            }, status=500)
    
    # Handle non-POST requests
    return JsonResponse({
        'success': False, 
        'message': 'Invalid request method'
    }, status=405)


@csrf_protect
@require_http_methods(["GET"])
def search_rides(request):
    try:
        pickup_location = request.GET.get('pickup_location')
        pickup_time = request.GET.get('pickup_time')
        
        db = RiderDatabase()
        rides = db.searchRides(
            pickup_location=pickup_location, 
            picktime=pickup_time
        )
        
        return JsonResponse({'success': True, 'rides': rides})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_protect
@require_http_methods(["GET"])
def rider_profile_view(request):
    try:
        # Get username from the request
        username = request.GET.get('username')
        
        if not username:
            return JsonResponse({
                'success': False,
                'message': 'Username is required'
            }, status=400)
        
        # Use RiderDatabase to fetch profile data
        rider_db = RiderDatabase()
        profile_data = rider_db.getProfileData(username)
        
        # Check if profile data was successfully retrieved
        if isinstance(profile_data, dict) and 'error' in profile_data:
            return JsonResponse({
                'success': False,
                'message': profile_data.get('error', 'Profile not found')
            }, status=404)
        
        # Prepare the response with full profile details
        return JsonResponse({
            'success': True,
            'profile': {
                'username': profile_data.get('username', 'N/A'),
                'name': profile_data.get('name', 'N/A'),
                'email': profile_data.get('email', 'N/A'),
                'phone': profile_data.get('phone', 'N/A'),
                'pickup_location': profile_data.get('pickup_location', 'N/A')
            }
        })
    
    except Exception as e:
        # Log the full error
        import traceback
        traceback.print_exc()
        
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500) 

@csrf_protect
@require_http_methods(["GET"])
def rider_bookings_view(request):
    try:
        username = request.GET.get('username')
        r = RiderDatabase()  # Ensure that r is an instance of RiderDatabase
        # Fetch rider's bookings
        bookings_data = r.getBookings(username)
        
        # Check if bookings were found
        if bookings_data is None:
            return JsonResponse({
                'success': False,
                'message': 'No bookings found'
            })
        
        return JsonResponse({
            'success': True,
            'bookings': bookings_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

@csrf_protect
@require_http_methods(["POST"])
def book_ride_view(request):
    try:
        data = json.loads(request.body)
        rider_username = data.get('rider_username')
        driver_username = data.get('driver_username')
        
        try:
            # Fetch Rider and Driver
            rider = Rider.objects.get(person__username=rider_username)
            driver = Driver.objects.get(person__username=driver_username)
            
            # Check if driver has available seats
            if driver.seats_available > 0:
                # Create booking
                booking = Booking.objects.create(driver=driver)
                booking.riders.add(rider)
                
                # Reduce available seats
                driver.seats_available -= 1
                driver.save()
                
                return JsonResponse({
                    'success': True, 
                    'message': 'Ride booked successfully'
                })
            else:
                return JsonResponse({
                    'success': False, 
                    'message': 'No seats available'
                })
        except (Rider.DoesNotExist, Driver.DoesNotExist):
            return JsonResponse({
                'success': False, 
                'message': 'Rider or Driver not found'
            })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': str(e)
        })


@csrf_protect
@require_http_methods(["GET"])
def search_rides_view(request):
    try:
        # Get search parameters
        pickup_location = request.GET.get('pickup_location', '').lower()
        car_make = request.GET.get('car_make', '').lower()
        
        # Use RiderDatabase to search rides
        rider_db = RiderDatabase()
        rides = rider_db.searchRides(
            pickup_location=pickup_location, 
            carMake=car_make
        )
        
        # Return search results
        return JsonResponse({
            'success': True, 
            'rides': rides
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': str(e)
        })

@csrf_protect
@require_http_methods(["POST"])
def book_ride(request):
    try:
        data = json.loads(request.body)
        rider_username = data.get('rider_username')
        driver_username = data.get('driver_username')
        
        db = RiderDatabase()
        success = db.storeBooking(rider_username, driver_username)
        
        if success:
            return JsonResponse({'success': True, 'message': 'Ride booked successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Booking failed'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


#driver dashboard  -----------------------------------------------------------------------
def driver_profile_view(request):
    try:
        # Get username from request
        username = request.GET.get('username')
        
        # Initialize DriverDatabase
        driver_db = DriverDatabase()
        
        # Fetch profile data
        profile_data = driver_db.getProfileData(username)
        
        if 'error' not in profile_data:
            return JsonResponse({
                'success': True,
                'profile': profile_data
            })
        else:
            return JsonResponse({
                'success': False,
                'message': profile_data['error']
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


def driver_bookings_view(request):
    """
    Fetch driver's current bookings with detailed rider information and rating
    """
    try:
        username = request.GET.get('username')
        
        if not username:
            return JsonResponse({
                'success': False,
                'message': 'Username is required'
            }, status=400)
        
        # Initialize databases
        driver_db = DriverDatabase()
        rider_db = RiderDatabase()
        
        # Fetch bookings for this driver
        bookings = driver_db.getBookings(username)
        
        # Convert bookings to a list of dictionaries
        booking_list = []
        for booking in bookings:
            # Get the first rider (assuming one rider per booking)
            try:
                # Fetch rider rating
                rider_rating = rider_db.getRating(booking['rider_username'])
                
                booking_info = {
                    'id': booking.get('id', 'N/A'),
                    'rider_username': booking['rider_username'],
                    'rider_name': booking['rider_name'],
                    'rider_phone': booking['rider_phone'],
                    'rider_location': booking['rider_location'],
                    'rider_rating': round(rider_rating, 2) if rider_rating is not None else '0'
                }
                booking_list.append(booking_info)
            except Exception as e:
                print(f"Error processing booking: {e}")
        
        return JsonResponse({
            'success': True,
            'bookings': booking_list
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


def update_driver_profile_view(request):
    """
    Update driver profile information
    """
    try:
        # Get updated profile data from request
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        car_model = request.POST.get('car_model')
        route = request.POST.get('route')
        
        # Initialize DriverDatabase
        driver_db = DriverDatabase()
        
        # Update profile methods
        email_updated = driver_db.setEmail(username, email)
        phone_updated = driver_db.setPhone(username, phone)
        car_model_updated = driver_db.setCarModel(username, car_model)
        route_updated = driver_db.setRoute(username, route)
        
        if email_updated and phone_updated and car_model_updated and route_updated:
            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Failed to update profile'
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })
    

def driver_bookings_view(request):
    """
    Fetch driver's current bookings
    """
    try:
        username = request.GET.get('username')
        driver_db = DriverDatabase()
        
        # Assuming you have a method to get driver bookings
        bookings = driver_db.getBookings(username)
        
        return JsonResponse({
            'success': True,
            'bookings': bookings
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


def driver_rate_rider_view(request):
    """
    Store rating for a rider
    """
    try:
        data = json.loads(request.body)
        from_username = data.get('from_username')
        to_username = data.get('to_username')
        score = data.get('score')
        feedback = data.get('feedback', '')
        
        driver_db = DriverDatabase()
        
        result = driver_db.storeRating(from_username, to_username, score, feedback)
        
        if result:
            return JsonResponse({
                'success': True,
                'message': 'Rating stored successfully'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Failed to store rating'
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })



@csrf_protect
@require_http_methods(["GET"])
def search_rides_view(request):
    try:
        pickup_location = request.GET.get('pickup_location', '').lower()
        car_make = request.GET.get('car_make', '').lower()
        
        # Fetch drivers
        drivers = Driver.objects.filter(seats_available__gt=0)
        if pickup_location:
            drivers = drivers.filter(route__icontains=pickup_location)
        if car_make:
            drivers = drivers.filter(car_model__icontains=car_make)
        
        # Prepare response data
        rides_list = []
        for driver in drivers:
            ratings = Rating.objects.filter(to_person=driver.person)
            avg_rating = ratings.aggregate(Avg('score'))['score__avg'] if ratings.exists() else None
            rides_list.append({
                'username': driver.person.username,
                'name': driver.person.name,
                'car_model': driver.car_model,
                'seats_available': driver.seats_available,
                'route': driver.route,
                'timing': driver.timing,
                'average_rating': round(avg_rating, 2) if avg_rating else None,
            })
        
        return JsonResponse({'success': True, 'rides': rides_list})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def rider_location_view(request):
    """
    Get rider's pickup location
    """
    try:
        username = request.GET.get('username')
        rider_db = RiderDatabase()
        
        location = rider_db.getLocation(username)
        
        if location:
            return JsonResponse({
                'success': True,
                'pickup_location': location
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Location not found'
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

def rider_rating_view(request):


    """
    Get rider's rating
    """
    try:
        username = request.GET.get('username')
        rider_db = RiderDatabase()
        
        rating = rider_db.getRating(username)
        
        return JsonResponse({
            'success': True,
            'rating': rating
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

@csrf_protect
@require_http_methods(["POST"])
def driver_cancel_booking_view(request):
    try:
        print(request.body)
        data = json.loads(request.body)
        rider_username = data.get('rider_username')
        driver_username = data.get('driver_username')
        print(rider_username)
        print(driver_username)
        # Input validation
        if not rider_username or not driver_username:
            return JsonResponse({
                'success': False,
                'message': 'Both rider and driver usernames are required'
            }, status=400)
        
        driver_db = DriverDatabase()
        
        # Cancel booking and get detailed result
        result = driver_db.deleteBooking(driver_username, rider_username)
        print(result)
        return JsonResponse(result, status=200 if result['success'] else 400)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    
    except Exception as e:
        # Return error message without logging
        return JsonResponse({
            'success': False,
            'message': 'An unexpected error occurred'
        }, status=500)

@csrf_protect
@require_http_methods(["POST"])
def rider_cancel_booking_view(request):
    try:
        data = json.loads(request.body)
        rider_username = data.get('rider_username')
        driver_username = data.get('driver_username')
        
        print(f"Attempting to cancel booking - Rider: {rider_username}, Driver: {driver_username}")
        
        rider_db = RiderDatabase()
        
        result = rider_db.deleteBooking(driver_username, rider_username)
        
        if result:
            return JsonResponse({
                'success': True,
                'message': 'Booking cancelled successfully'
            })
        else:
            print(f"Failed to cancel booking for Rider: {rider_username}, Driver: {driver_username}")
            return JsonResponse({
                'success': False,
                'message': 'Failed to cancel booking. No matching booking found.'
            })
    except Exception as e:
        print(f"Exception in booking cancellation: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        })