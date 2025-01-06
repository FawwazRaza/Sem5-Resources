// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    console.log('yes');
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
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

// Fetch Rider Profile
async function fetchRiderProfile() {
    try {
        const username = localStorage.getItem('username');
        
        if (!username) {
            console.error('No username found');
            window.location.href = '/login/';
            return;
        }

        const response = await fetch(`/api/rider/profile/?username=${username}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Rider Profile Data:', data);

        if (data.success) {
            const profile = data.profile;
            // fetchMyBookings();
            // Update profile details
            document.getElementById('rider-username').textContent = profile.username || 'N/A';
            document.getElementById('rider-name').textContent = profile.name || 'N/A';
            document.getElementById('rider-email').textContent = profile.email || 'N/A';
            document.getElementById('rider-phone').textContent = profile.phone || 'N/A';
            document.getElementById('rider-pickup-location').textContent = profile.pickup_location || 'N/A';
        } else {
            console.error('Failed to fetch rider profile:', data.message);
            
            // Set default values if fetch fails
            document.getElementById('rider-username').textContent = 'N/A';
            document.getElementById('rider-name').textContent = 'N/A';
            document.getElementById('rider-email').textContent = 'N/A';
            document.getElementById('rider-phone').textContent = 'N/A';
            document.getElementById('rider-pickup-location').textContent = 'N/A';
        }
    } catch (error) {
        console.error('Rider profile fetch error:', error);
        
        // Set default values on error
        document.getElementById('rider-username').textContent = 'N/A';
        document.getElementById('rider-name').textContent = 'N/A';
        document.getElementById('rider-email').textContent = 'N/A';
        document.getElementById('rider-phone').textContent = 'N/A';
        document.getElementById('rider-pickup-location').textContent = 'N/A';
    }
}


async function fetchMyBookings() {
    try {
        const username = localStorage.getItem('username');
        
        // Check if username exists
        if (!username) {
            throw new Error('No username found. Please log in.');
        }

        const response = await fetch(`/api/rider/bookings/?username=${encodeURIComponent(username)}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin' // Important for including cookies
        });

        // Check if response is ok
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Bookings Data rider:', data);

        const bookingsList = document.getElementById('bookings-list');
        bookingsList.innerHTML = ''; // Clear previous results only once

        // Check if data has success and bookings array
        if (data.success && data.bookings && data.bookings.length > 0) {
            // Iterate through the bookings array
            data.bookings.forEach(booking => {
                const bookingElement = document.createElement('div');
                bookingElement.classList.add('booking-item', 'card', 'mb-3');
                bookingElement.innerHTML = `
                    <div class="card-header">
                        <h3>Booking with ${booking.driver_name || 'Unknown Driver'}</h3>
                    </div>
                    <div class="card-body">
                        <p><strong>Driver Username:</strong> ${booking.driver_username || 'N/A'}</p>
                        <p><strong>Driver Phone:</strong> ${booking.driver_phone || 'N/A'}</p>
                        <p><strong>Car:</strong> ${booking.car_model || 'N/A'}</p>
                        <p><strong>Route:</strong> ${formatRoute(booking.route)}</p>
                        <p><strong>Booking ID:</strong> ${booking.id || 'N/A'}</p>
                        <button class="btn btn-danger" onclick="openCancelBookingModal('${booking.driver_username}')">Cancel Booking</button>
                    </div>
                `;
                
                bookingsList.appendChild(bookingElement);
            });
        } else {
            bookingsList.innerHTML = `
                <div class="alert alert-info" role="alert">
                    No bookings found. Would you like to book a ride?
                </div>
            `;
        }
    } catch (error) {
        console.error('Fetch bookings error:', error);
        
        const bookingsList = document.getElementById('bookings-list');
        bookingsList.innerHTML = `
            <div class="alert alert-danger" role="alert">
                ${error.message || 'Error fetching bookings. Please try again later.'}
            </div>
        `;
    }
}

// Utility function to format route (assuming route is an array)

function formatRoute(route) {
    // If route is an array, join its elements, otherwise return a default message
    return route && route.length > 0 ? route.join(' → ') : 'No route information';
}

// Optional: Add a way to refresh bookings periodically
function setupBookingsRefresh() {
    fetchMyBookings(); // Initial fetch
    setInterval(fetchMyBookings, 5 * 60 * 1000); // Refresh every 5 minutes
}

// Call this when the page loads
document.addEventListener('DOMContentLoaded', setupBookingsRefresh);
// Search Rides Function
async function searchRides() {
    const pickupLocation = document.getElementById('pickup-location').value;
    const carMake = document.getElementById('car-make').value;

    try {
        const response = await fetch(`/api/rider/search-rides/?pickup_location=${pickupLocation}&car_make=${carMake}`, {
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
            document.getElementById('rides-list').innerHTML = '<p>No rides found</p>';
        }
    } catch (error) {
        console.error('Search rides error:', error);
        document.getElementById('rides-list').innerHTML = '<p>Error searching rides</p>';
    }
}

// Display Rides Function
function displayRides(rides) {
    const ridesList = document.getElementById('rides-list');
    ridesList.innerHTML = ''; // Clear previous results

    if (!rides || rides.length === 0) {
        ridesList.innerHTML = '<p>No rides found</p>';
        return;
    }

    rides.forEach(ride => {
        const rideElement = document.createElement('div');
        rideElement.classList.add('ride-card');
        rideElement.innerHTML = `
            <h3>Driver: ${ride.name || 'N/A'}</h3>
            <p>Car Model: ${ride.car_model || 'N/A'}</p>
            <p>Seats Available: ${ride.seats_available || 'N/A'}</p>
            <p>Route: ${ride.route || 'N/A'}</p>
            <p>Timing: ${ride.timing || 'N/A'}</p>
            <p>Rating: ${ride.average_rating || 'N/A'}</p>
            <button onclick="bookRide('${ride.username}')">Book Ride</button>
        `;
        ridesList.appendChild(rideElement);
    });
}

// Book Ride Function
async function bookRide(driverUsername) {
    try {
        const riderUsername = localStorage.getItem('username');
        const response = await fetch('/api/book-ride/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                rider_username: riderUsername,
                driver_username: driverUsername
            })
        });

        const data = await response.json();
        console.log('Book Ride Response:', data);

        if (data.success) {
            alert('Ride booked successfully!');
            fetchMyBookings(); // Refresh bookings
        } else {
            alert(data.message || 'Booking failed');
        }
    } catch (error) {
        console.error('Book ride error:', error);
        alert('An error occurred while booking the ride');
    }
}

// Function to open cancel booking modal
function openCancelBookingModal() {
    const modalContainer = document.getElementById('modal-container');
    modalContainer.innerHTML = `
        <div class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Cancel Booking</h2>
                    <button onclick="closeModal()">&times;</button>
                </div>
                <div>
                    <input 
                        type="text" 
                        id="cancel-driver-username" 
                        class="modal-input" 
                        placeholder="Enter Driver Username"
                    >
                </div>
                <div class="modal-actions">
                    <button onclick="cancelBooking()" class="btn">Confirm Cancel</button>
                    <button onclick="closeModal()" class="btn">Close</button>
                </div>
            </div>
        </div>
    `;
}

// Function to close modal
function closeModal() {
    const modalContainer = document.getElementById('modal-container');
    modalContainer.innerHTML = '';
}

async function cancelBooking() {
    const driverUsernameInput = document.getElementById('cancel-driver-username');
    const driverUsername = driverUsernameInput ? driverUsernameInput.value.trim() : null;
    console.log('Rider Username:', driverUsername)
    try {
        const riderUsername = localStorage.getItem('username');
        
        // Validate inputs
        if (!riderUsername) {
            alert('Rider username not found. Please log in again.');
            return;
        }
        
        if (!driverUsername) {
            alert('Please enter a driver username');
            return;
        }
        
        // Send request to backend to cancel booking
        const response = await fetch('/api/rider/cancel-booking/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ 
                rider_username: riderUsername,
                driver_username: driverUsername 
            })
        });

        const responseData = await response.json();

        // Handle response
        if (responseData.success) {
            alert('Booking cancelled successfully!');
            closeModal();
            // Refresh bookings list
            fetchMyBookings();
        } else {
            // Show error message from backend or a generic message
            alert(responseData.message || 'Cancellation failed');
        }
    } catch (error) {
        console.error('Cancel booking error:', error);
        alert('An error occurred while cancelling the booking');
    }
}
async function logout() {
    try {
        const response = await fetch('/api/logout/', {
            method: 'POST',
            headers: { 
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        });
        const data = await response.json();
        if (data.success) {
            localStorage.removeItem('username');
            localStorage.removeItem('user_type');
            window.location.href = '/login/';
        } else {
            alert('Logout failed');
        }
    } catch (error) {
        console.error('Logout error:', error);
        alert('An error occurred during logout');
    }
}

// Event Listeners and Initial Load
document.addEventListener('DOMContentLoaded', () => {
    const username = localStorage.getItem('username');
    const userType = localStorage.getItem('user_type');

    // Debug logging
    console.log('Username:', username);
    console.log('User Type:', userType);

    if (!username || userType !== 'Rider') {
        console.warn('Redirecting to login - invalid session');
        window.location.href = '/login/';
        return;
    }

    // Call the profile fetch function
    fetchRiderProfile();
    // fetchMyBookings();
    // Add event listeners
    document.getElementById('search-rides-btn')?.addEventListener('click', searchRides);
    document.getElementById('fetch-bookings-btn')?.addEventListener('click', fetchMyBookings);
    document.getElementById('logout-btn')?.addEventListener('click', logout);
});