document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const userType = document.getElementById('user-type').value;

    // Client-side validation
    if (!username || !password) {
        alert('Please enter both username and password');
        return;
    }

    try {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                username: username,
                password: password,
                user_type: userType
            })
        });

        const data = await response.json();
        console.log('Login Response:', data);

        if (data.success) {
            // Store user information in localStorage for session tracking
            localStorage.setItem('username', username);
            localStorage.setItem('user_type', userType);

            // Redirect based on user type
            if (userType === 'Driver') {
                window.location.href = '/driver/dashboard/';
            } else {
                window.location.href = '/rider/dashboard/';
            }
        } else {
            // Display server-provided error message or default message
            alert(data.message || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An unexpected error occurred during login');
    }
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            console.log('hi');
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
