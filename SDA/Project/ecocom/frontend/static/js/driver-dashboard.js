// Utility function to get CSRF cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                console.log('Cookie:', cookie);
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to fetch driver profile
async function fetchDriverProfile() {
    try {
        const username = localStorage.getItem('username');
        
        if (!username) {
            console.error('No username found');
            window.location.href = '/login/';
            return null;
        }

        const response = await fetch(`/api/driver/profile/?username=${username}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const data = await response.json();

        if (data.success) {
            const profile = data.profile;
            
            // Store name in localStorage
            localStorage.setItem('name', profile.name);

            // Update profile details
            updateProfileUI(profile);

            return profile;
        } else {
            console.error('Failed to fetch driver profile:', data.message);
            alert(data.message || 'Failed to load profile');
            return null;
        }
    } catch (error) {
        console.error('Profile fetch error:', error);
        alert('An error occurred while fetching profile');
        return null;
    }
}

// Function to update UI with profile details
function updateProfileUI(profile) {
    // Helper function to set text content safely
    const setElementText = (id, value) => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value || 'N/A';
        }
    };

    // Update all profile fields
    setElementText('profile-username', profile.username);
    setElementText('profile-name', profile.name);
    setElementText('profile-email', profile.email);
    setElementText('profile-phone', profile.phone);
    setElementText('profile-car-model', profile.car_model);
    setElementText('profile-car-license', profile.car_license);
    setElementText('profile-seats', profile.seats_available);
    
    // Special handling for route (might be an array)
    const routeElement = document.getElementById('profile-route');
    if (routeElement) {
        routeElement.textContent = Array.isArray(profile.route) 
            ? profile.route.join(', ') 
            : (profile.route || 'N/A');
    }

    setElementText('profile-schedule', profile.schedule);
}

async function fetchDriverBookings() {
    try {
        const username = localStorage.getItem('username');
        
        if (!username) {
            console.error('No username found');
            window.location.href = '/login/';
            return;
        }

        const response = await fetch(`/api/driver/bookings/?username=${username}`, {
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
        console.log('Driver Bookings Data:', data);

        const bookingsList = document.getElementById('bookings-list');
        bookingsList.innerHTML = ''; // Clear previous results

        if (data.success && data.bookings && data.bookings.length > 0) {
            const uniqueBookings = new Set(); // Use Set to prevent duplicates
            data.bookings.forEach(booking => {
                // Store rider details in sessionStorage
                sessionStorage.setItem(
                    `rider_${booking.id}`, 
                    JSON.stringify({
                        username: booking.rider_username,
                        name: booking.rider_name,
                        phone: booking.rider_phone,
                        location: booking.rider_location
                    })
                );

                // Check if booking is already added
                if (!uniqueBookings.has(booking.id)) {
                    uniqueBookings.add(booking.id);
                    const bookingElement = document.createElement('div');
                    bookingElement.classList.add('booking-item');
                    bookingElement.innerHTML = `
                        <div class="booking-details">
                            <h3>Booking with ${booking.rider_name}</h3>
                            <div class="rider-info">
                                <h4>Rider Details</h4>
                                <p><strong>Username:</strong> ${booking.rider_username}</p>
                                <p><strong>Name:</strong> ${booking.rider_name}</p>
                                <p><strong>Phone:</strong> ${booking.rider_phone}</p>
                                <p><strong>Pickup Location:</strong> ${booking.rider_location}</p>
                            </div>
                            <div class="booking-actions">
                                <button onclick="openCancelBookingModal()">Cancel Booking</button>
                                <button onclick="rateRider('${booking.rider_username}')">Rate Rider</button>
                            </div>
                        </div>
                    `;
                    bookingsList.appendChild(bookingElement);
                }
            });
        } else {
            bookingsList.innerHTML = '<p>No bookings found</p>';
        }
    } catch (error) {
        console.error('Fetch driver bookings error:', error);
        const bookingsList = document.getElementById('bookings-list');
        bookingsList.innerHTML = '<p>Error fetching bookings</p>';
    }
}

async function fetchRiderDetails(username) {
    try {
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
        
        if (data.success) {
            return data;
        } else {
            console.error('Failed to fetch rider details:', data.message);
            return { 
                success: false, 
                profile: { 
                    name: 'N/A', 
                    email: 'N/A', 
                    phone: 'N/A', 
                    pickup_location: 'N/A' 
                } 
            };
        }
    } catch (error) {
        console.error('Fetch rider details error:', error);
        return { 
            success: false, 
            profile: { 
                name: 'N/A', 
                email: 'N/A', 
                phone: 'N/A', 
                pickup_location: 'N/A' 
            } 
        };
    }
}
// Updated cancelBooking function to handle manual username input
async function cancelBooking() {
    const riderUsernameInput = document.getElementById('cancel-rider-username');
    const riderUsername = riderUsernameInput ? riderUsernameInput.value.trim() : null;
    console.log('Rider Username:', riderUsername);
    try {
        const driverUsername = localStorage.getItem('username');
        console.log('Driver Username:', driverUsername);
        // Validate usernames
        if (!driverUsername || !riderUsername) {
            alert('Please enter a rider username');
            return;
        }
        
        const response = await fetch('/api/driver/cancel-booking/', {
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

        if (data.success) {
            alert('Booking cancelled successfully!');
            // Close the modal
            closeModal();
            // Refresh bookings list
            fetchDriverBookings();
        } else {
            alert(data.message || 'Cancellation failed');
        }
    } catch (error) {
        console.error('Cancel booking error:', error);
        alert('An error occurred while cancelling the booking');
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
                        id="cancel-rider-username" 
                        class="modal-input" 
                        placeholder="Enter Rider Username"
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


function renderBookings(bookings) {
    const bookingsList = document.getElementById('bookings-list');
    bookingsList.innerHTML = ''; // Clear previous results

    if (bookings && bookings.length > 0) {
        bookings.forEach(booking => {
            const bookingElement = document.createElement('div');
            bookingElement.classList.add('booking-item');
            bookingElement.innerHTML = `
                <div class="booking-details">
                    <h3>Booking with ${booking.rider_name}</h3>
                    <div class="rider-info">
                        <h4>Rider Details</h4>
                        <p><strong>Username:</strong> ${booking.rider_username}</p>
                        <p><strong>Name:</strong> ${booking.rider_name}</p>
                        <button onclick="cancelBooking('${booking.rider_username}', '${localStorage.getItem('username')}')">
                            Cancel Booking
                        </button>
                    </div>
                </div>
            `;
            bookingsList.appendChild(bookingElement);
        });
    } else {
        bookingsList.innerHTML = '<p>No bookings found</p>';
    }
}

// Function to rate a rider
function rateRider(riderUsername) {
    // Create rating modal
    const ratingsList = document.getElementById('rider-ratings-list');
    ratingsList.innerHTML = `
        <div class="rating-modal">
            <h3>Rate Rider</h3>
            <form id="rider-rating-form">
                <div class="rating-stars">
                    <input type="radio" name="rating" value="1" id="star1">
                    <label for="star1">★</label>
                    <input type="radio" name="rating" value="2" id="star2">
                    <label for="star2">★</label>
                    <input type="radio" name="rating" value="3" id="star3">
                    <label for="star3">★</label>
                    <input type="radio" name="rating" value="4" id="star4">
                    <label for="star4">★</label>
                    <input type="radio" name="rating" value="5" id="star5">
                    <label for="star5">★</label>
                </div>
                <textarea id="rating-feedback" placeholder="Optional feedback"></textarea>
                <div class="rating-actions">
                    <button type="button" onclick="submitRiderRating('${riderUsername}')">Submit Rating</button>
                    <button type="button" onclick="closeRatingModal()">Cancel</button>
                </div>
            </form>
        </div>
    `;
}

// Function to submit rider rating
async function submitRiderRating(riderUsername) {
    try {
        const selectedRating = document.querySelector('input[name="rating"]:checked');
        const feedbackElement = document.getElementById('rating-feedback');
        
        if (!selectedRating) {
            alert('Please select a rating');
            return;
        }

        const response = await fetch('/api/driver/rate-rider/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                from_username: localStorage.getItem('username'),
                to_username: riderUsername,
                score: parseInt(selectedRating.value),
                feedback: feedbackElement.value || ''
            })
        });

        const data = await response.json();

        if (data.success) {
            alert('Rating submitted successfully');
            closeRatingModal();
        } else {
            alert('Failed to submit rating');
        }
    } catch (error) {
        console.error('Rating submission error:', error);
        alert('An error occurred while submitting rating');
    }
}

// Function to close rating modal
function closeRatingModal() {
    const ratingsList = document.getElementById('rider-ratings-list');
    ratingsList.innerHTML = '';
}

// DOMContentLoaded event listener
document.addEventListener('DOMContentLoaded', () => {
    const username = localStorage.getItem('username');
    const userType = localStorage.getItem('user_type');

    // Check if user is logged in and is a driver
    if (!username || userType !== 'Driver') {
        window.location.href = '/login/';
        return;
    }

    // Fetch driver profile and bookings
    Promise.all([
        fetchDriverProfile(), 
        fetchDriverBookings(),
    ]).then(() => {
        console.log('Driver profile and bookings loaded');
    }).catch(error => {
        console.error('Error loading driver data:', error);
    });

    // Logout functionality
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/api/logout/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    }
                });

                const data = await response.json();
                
                if (data.success) {
                    // Clear all stored user data
                    localStorage.removeItem('username');
                    localStorage.removeItem('name');
                    localStorage.removeItem('user_type');
                    window.location.href = '/login/';
                } else {
                    alert('Logout failed');
                }
            } catch (error) {
                console.error('Logout error:', error);
                alert('An error occurred during logout');
            }
        });
    }
});