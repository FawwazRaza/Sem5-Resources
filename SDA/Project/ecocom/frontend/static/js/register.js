
function getCookie(name) {
    let cookieValue = null;
    console.log('ok 100');
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        console.log('ok 200');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Form Interactions
function toggleDriverFields() {
    const userType = document.getElementById('user-type').value;
    const driverFields = document.getElementById('driver-fields');

    if (userType === 'Driver') {
        driverFields.style.display = 'block';
    } else {
        driverFields.style.display = 'none';
    }
}

// Registration Handler
async function handleRegistration(e) {
    e.preventDefault();

    // Collect common form data
    const formData = {
        username: document.getElementById('username').value,
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        password: document.getElementById('password').value,
        person_type: document.getElementById('user-type').value
    };

    // Validate common fields
    const errors = [];
    if (!formData.username) errors.push('Username is required');
    if (!formData.name) errors.push('Name is required');
    if (!formData.email) errors.push('Email is required');
    if (!formData.phone) errors.push('Phone is required');
    if (!formData.password) errors.push('Password is required');

    // Add driver-specific fields if user is a driver
    if (formData.person_type === 'Driver') {
        formData.car_model = document.getElementById('car-model').value;
        formData.car_license = document.getElementById('car-license').value;
        formData.seats_available = document.getElementById('seats').value;

        if (!formData.car_model) errors.push('Car model is required for drivers');
        if (!formData.car_license) errors.push('Car license is required for drivers');
        if (!formData.seats_available) errors.push('Number of seats is required for drivers');
    }

    // Display validation errors if any
    if (errors.length > 0) {
        alert(errors.join('\n'));
        return;
    }

    try {
        const response = await fetch('/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        console.log('Registration Response:', data);

        if (data.success) {
            alert('Registration Successful!');
            window.location.href = '/login/';
        } else {
            alert(data.message || 'Registration failed');
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('An unexpected error occurred during registration');
    }
}

// Ride Search Functions
async function searchRides() {
    const pickupLocation = document.getElementById('pickup-location').value;
    const pickupTime = document.getElementById('pickup-time').value;
    const carMake = document.getElementById('car-make').value;

    try {
        const response = await fetch(`/api/rider/search-rides/?pickup_location=${pickupLocation}&pickup_time=${pickupTime}&car_make=${carMake}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const data = await response.json();

        if (data.success) {
            displayRides(data.rides);
        } else {
            alert(`Error: ${data.message}`);
        }
    } catch (error) {
        console.error('Search rides error:', error);
        alert('An error occurred while searching for rides');
    }
}

function displayRides(rides) {
    const ridesList = document.getElementById('rides-list');
    ridesList.innerHTML = ''; // Clear previous results

    if (rides.length === 0) {
        ridesList.innerHTML = '<p>No rides found</p>';
        return;
    }

    rides.forEach(ride => {
        const rideElement = document.createElement('div');
        rideElement.classList.add('ride-item');
        rideElement.innerHTML = `
            <h3>Driver: ${ride.name}</h3>
            <p>Car Model: ${ride.car_model}</p>
            <p>Seats Available: ${ride.seats_available}</p>
            <p>Route: ${ride.route}</p>
            <p>Timing: ${ride.timing}</p>
            <button onclick="bookRide('${ride.username}')">Book Ride</button>
        `;
        ridesList.appendChild(rideElement);
    });
}

// Rider Information Functions
async function fetchRiderLocation() {
    try {
        const username = localStorage.getItem('username');
        const response = await fetch(`/api/rider/location/?username=${username}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('current-location').textContent = data.pickup_location;
        } else {
            console.error('Location fetch error:', data.message);
        }
    } catch (error) {
        console.error('Location fetch error:', error);
    }
}

async function fetchRiderRating() {
    try {
        const username = localStorage.getItem('username');
        const response = await fetch(`/api/rider/rating/?username=${username}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('rider-rating').textContent = data.rating.toFixed(2);
        } else {
            console.error('Rating fetch error:', data.message);
        }
    } catch (error) {
        console.error('Rating fetch error:', error);
    }
}

// Booking Management
async function fetchRiderBookings() {
    try {
        const username = localStorage.getItem('username');
        const response = await fetch(`/api/rider/bookings/?username=${username}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const data = await response.json();

        if (data.success) {
            displayBookings(data.bookings);
        } else {
            console.error('Bookings fetch error:', data.message);
        }
    } catch (error) {
        console.error('Bookings fetch error:', error);
    }
}

function displayBookings(bookings) {
    const bookingsList = document.getElementById('bookings-list');
    bookingsList.innerHTML = '';

    if (bookings.length === 0) {
        bookingsList.innerHTML = '<p>No active bookings</p>';
        return;
    }

    bookings.forEach(booking => {
        const bookingElement = document.createElement('div');
        bookingElement.classList.add('booking-item');
        bookingElement.innerHTML = `
            <h3>Booking with ${booking.driver_name}</h3>
            <p>Route: ${booking.route}</p>
            <p>Time: ${booking.time}</p>
            <button onclick="cancelBooking('${booking.id}')">Cancel Booking</button>
        `;
        bookingsList.appendChild(bookingElement);
    });
}

async function cancelBooking(bookingId) {
    try {
        const username = localStorage.getItem('username');
        const response = await fetch('/api/rider/cancel-booking/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ 
                username,
                booking_id: bookingId 
            })
        });

        const data = await response.json();

        if (data.success) {
            alert('Booking cancelled successfully');
            fetchRiderBookings(); // Refresh bookings
        } else {
            alert(`Error: ${data.message}`);
        }
    } catch (error) {
        console.error('Cancel booking error:', error);
        alert('An error occurred while cancelling the booking');
    }
}

async function bookRide(driverUsername) {
    try {
        const username = localStorage.getItem('username');
        const response = await fetch('/api/rider/book-ride/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ 
                rider_username: username,
                driver_username: driverUsername 
            })
        });

        const data = await response.json();

        if (data.success) {
            alert('Ride booked successfully!');
            fetchRiderBookings(); // Refresh bookings
        } else {
            alert(`Error: ${data.message}`);
        }
    } catch (error) {
        console.error('Book ride error:', error);
        alert('An error occurred while booking the ride');
    }
}

// Event Listeners and Initial Setup
document.addEventListener('DOMContentLoaded', () => {
    // Registration Form
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegistration);
    }

    // User Type Toggle
    const userTypeSelect = document.getElementById('user-type');
    if (userTypeSelect) {
        userTypeSelect.addEventListener('change', toggleDriverFields);
    }

    // Ride Search
    const searchRidesBtn = document.getElementById('search-rides-btn');
    if (searchRidesBtn) {
        searchRidesBtn.addEventListener('click', searchRides);
    }

    // Rider-specific data (only load if logged in)
    const username = localStorage.getItem('username');
    if (username) {
        fetchRiderLocation();
        fetchRiderRating();
        fetchRiderBookings();
    }
});