// Navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    // Navigation link switching
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links and sections
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Show corresponding section
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.classList.add('active');
            }
        });
    });
});

// Modal functionality
function showLoginModal() {
    document.getElementById('loginModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function showRegisterModal() {
    document.getElementById('registerModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    
    if (event.target == loginModal) {
        closeModal('loginModal');
    }
    if (event.target == registerModal) {
        closeModal('registerModal');
    }
}

// Tab switching for login modal
function switchLoginTab(type) {
    const studentForm = document.getElementById('studentLoginForm');
    const hotelForm = document.getElementById('hotelLoginForm');
    const tabBtns = document.querySelectorAll('#loginModal .tab-btn');
    
    // Remove active class from all forms and tabs
    studentForm.classList.remove('active');
    hotelForm.classList.remove('active');
    tabBtns.forEach(btn => btn.classList.remove('active'));
    
    // Show selected form and activate tab
    if (type === 'student') {
        studentForm.classList.add('active');
        tabBtns[0].classList.add('active');
    } else {
        hotelForm.classList.add('active');
        tabBtns[1].classList.add('active');
    }
}

// Tab switching for register modal
function switchRegisterTab(type) {
    const studentForm = document.getElementById('studentRegisterForm');
    const hotelForm = document.getElementById('hotelRegisterForm');
    const tabBtns = document.querySelectorAll('#registerModal .tab-btn');
    
    // Remove active class from all forms and tabs
    studentForm.classList.remove('active');
    hotelForm.classList.remove('active');
    tabBtns.forEach(btn => btn.classList.remove('active'));
    
    // Show selected form and activate tab
    if (type === 'student') {
        studentForm.classList.add('active');
        tabBtns[0].classList.add('active');
    } else {
        hotelForm.classList.add('active');
        tabBtns[1].classList.add('active');
    }
}

// Form submission handlers
document.addEventListener('DOMContentLoaded', function() {
    // Student login form
    const studentLoginForm = document.getElementById('studentLoginForm');
    if (studentLoginForm) {
        studentLoginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/login', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert(data.message || 'Login failed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during login');
            });
        });
    }

    // Hotel login form
    const hotelLoginForm = document.getElementById('hotelLoginForm');
    if (hotelLoginForm) {
        hotelLoginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Hotel login form submitted');
            
            const formData = new FormData(this);
            formData.append('user_type', 'hotel');
            console.log('Login data:', Object.fromEntries(formData));
            
            fetch('/login', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log('Hotel login response:', data);
                if (data.success) {
                    alert('Hotel login successful!');
                    window.location.reload();
                } else {
                    alert(data.message || 'Login failed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during login');
            });
        });
    } else {
        console.log('Hotel login form not found');
    }

    // Student registration form
    const studentRegisterForm = document.getElementById('studentRegisterForm');
    if (studentRegisterForm) {
        studentRegisterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/register', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Registration successful! Please login.');
                    closeModal('registerModal');
                    showLoginModal();
                } else {
                    alert(data.message || 'Registration failed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during registration');
            });
        });
    }

    // Hotel registration form
    const hotelRegisterForm = document.getElementById('hotelRegisterForm');
    if (hotelRegisterForm) {
        hotelRegisterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/register-hotel', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Hotel registration successful! Please login.');
                    closeModal('registerModal');
                    showLoginModal();
                } else {
                    alert(data.message || 'Registration failed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during registration');
            });
        });
    }
});

// Smooth scrolling for internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Post interactions
function likePost(postId) {
    // Add like functionality
}

function commentPost(postId) {
    // Add comment functionality
}

function sharePost(postId) {
    // Add share functionality
}

// Dashboard functionality
function showDashboard() {
    document.getElementById('dashboardModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // First check what type of user is logged in
    fetch('/get-profile')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.type === 'hotel') {
                    // Hotel owner dashboard
                    document.getElementById('studentDashboard').style.display = 'none';
                    document.getElementById('hotelDashboard').style.display = 'block';
                    document.getElementById('dashboardTitle').textContent = 'Hotel Dashboard';
                    
                    // Load hotel menu and stats
                    loadDashboardContent();
                } else {
                    // Student dashboard
                    document.getElementById('studentDashboard').style.display = 'block';
                    document.getElementById('hotelDashboard').style.display = 'none';
                    document.getElementById('dashboardTitle').textContent = 'My Dashboard';
                    
                    // Load student posts
                    loadDashboardContent();
                }
            } else {
                // Fallback - try both approaches
                tryLoadStudentDashboard();
            }
        })
        .catch(error => {
            console.error('Error checking profile:', error);
            // Fallback - try both approaches
            tryLoadStudentDashboard();
        });
}

function tryLoadStudentDashboard() {
    // Check user type and show appropriate dashboard
    fetch('/my-posts')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Student dashboard
                document.getElementById('studentDashboard').style.display = 'block';
                document.getElementById('hotelDashboard').style.display = 'none';
                document.getElementById('dashboardTitle').textContent = 'My Dashboard';
                displayUserReviews(data.reviews);
                displayUserFoods(data.food_posts);
            }
        })
        .catch(error => {
            // Try hotel dashboard
            fetch('/my-menu')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Hotel dashboard
                        document.getElementById('studentDashboard').style.display = 'none';
                        document.getElementById('hotelDashboard').style.display = 'block';
                        document.getElementById('dashboardTitle').textContent = 'Hotel Dashboard';
                        displayHotelMenu(data.menu_items);
                        loadMenuStats(); // Load stats for hotel dashboard
                    }
                })
                .catch(error => console.error('Error loading dashboard:', error));
        });
}

function showPostReviewModal() {
    document.getElementById('postReviewModal').style.display = 'block';
    loadRestaurants();
}

function showPostFoodModal() {
    document.getElementById('postFoodModal').style.display = 'block';
}

function showAddMenuModal() {
    document.getElementById('addMenuModal').style.display = 'block';
    console.log('Add menu modal opened');
}

// Delete menu item function
function deleteMenuItem(itemId) {
    if (!confirm('Are you sure you want to delete this menu item? This action cannot be undone.')) {
        return;
    }
    
    fetch(`/delete-menu-item/${itemId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Menu item deleted successfully!');
            loadDashboardContent(); // Refresh the dashboard
        } else {
            alert(data.message || 'Failed to delete menu item');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the menu item');
    });
}

// Toggle menu availability function
function toggleMenuAvailability(itemId) {
    fetch(`/toggle-menu-availability/${itemId}`, {
        method: 'PUT'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            loadDashboardContent(); // Refresh the dashboard
        } else {
            alert(data.message || 'Failed to update menu item');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the menu item');
    });
}

// Load menu statistics
function loadMenuStats() {
    fetch('/menu-stats')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const stats = data.stats;
                document.getElementById('totalItems').textContent = stats.total_items;
                document.getElementById('activeItems').textContent = stats.active_items;
                document.getElementById('expiredItems').textContent = stats.expired_items;
                document.getElementById('recentReviews').textContent = stats.recent_reviews;
            } else {
                console.error('Failed to load stats:', data.message);
            }
        })
        .catch(error => {
            console.error('Error loading stats:', error);
        });
}

// Manual cleanup function
function manualCleanup() {
    if (!confirm('This will permanently delete all expired menu items, reviews, and posts. Continue?')) {
        return;
    }
    
    fetch('/cleanup-expired', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            loadMenuStats(); // Refresh stats
            loadDashboardContent(); // Refresh dashboard
        } else {
            alert(data.message || 'Cleanup failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during cleanup');
    });
}

// Test hotel login function (debugging)
function testHotelLogin() {
    fetch('/test-hotel-login')
        .then(response => response.json())
        .then(data => {
            console.log('Hotel login test:', data);
            alert(JSON.stringify(data, null, 2));
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error testing hotel login');
        });
}

function showSettingsModal() {
    document.getElementById('settingsModal').style.display = 'block';
    loadUserProfile();
}

function showHotelSettingsModal() {
    document.getElementById('hotelSettingsModal').style.display = 'block';
    loadBusinessProfile();
}

// Load user profile for settings
function loadUserProfile() {
    fetch('/get-profile')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.type === 'student') {
                document.getElementById('settingsUsername').value = data.user.username || '';
                document.getElementById('settingsRegNumber').value = data.user.reg_number || '';
                document.getElementById('settingsEmail').value = data.user.email || '';
            }
        })
        .catch(error => console.error('Error loading profile:', error));
}

// Load business profile for settings
function loadBusinessProfile() {
    fetch('/get-profile')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.type === 'hotel') {
                document.getElementById('businessUsername').value = data.user.username || '';
                document.getElementById('businessName').value = data.user.hotel_name || '';
                document.getElementById('businessEmail').value = data.user.email || '';
                document.getElementById('businessAddress').value = data.user.hotel_address || '';
                document.getElementById('businessContact').value = data.user.contact_number || '';
                document.getElementById('businessLicense').value = data.user.license_number || '';
            }
        })
        .catch(error => console.error('Error loading business profile:', error));
}

// Dashboard tab switching
function switchDashboardTab(tab) {
    // Remove active class from all tabs
    document.querySelectorAll('#studentDashboard .dashboard-tabs .tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('#studentDashboard .dashboard-tab-content').forEach(content => content.classList.remove('active'));
    
    // Add active class to selected tab
    event.target.classList.add('active');
    document.getElementById(tab + 'Tab').classList.add('active');
}

// Hotel dashboard tab switching
function switchHotelTab(tab) {
    // Remove active class from all tabs
    document.querySelectorAll('#hotelDashboard .dashboard-tabs .tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('#hotelDashboard .dashboard-tab-content').forEach(content => content.classList.remove('active'));
    
    // Add active class to selected tab
    event.target.classList.add('active');
    document.getElementById(tab + 'Tab').classList.add('active');
}

// Settings tab switching
function switchSettingsTab(tab) {
    // Remove active class from all tabs
    document.querySelectorAll('#settingsModal .settings-tabs .tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('#settingsModal .settings-tab-content').forEach(content => content.classList.remove('active'));
    
    // Add active class to selected tab
    event.target.classList.add('active');
    document.getElementById(tab + 'SettingsTab').classList.add('active');
}

// Hotel settings tab switching
function switchHotelSettingsTab(tab) {
    // Remove active class from all tabs
    document.querySelectorAll('#hotelSettingsModal .settings-tabs .tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('#hotelSettingsModal .settings-tab-content').forEach(content => content.classList.remove('active'));
    
    // Add active class to selected tab
    event.target.classList.add('active');
    document.getElementById(tab + 'SettingsTab').classList.add('active');
}

// Load dashboard content
function loadDashboardContent() {
    // Check if it's a hotel dashboard
    const hotelDashboard = document.getElementById('hotelDashboard');
    if (hotelDashboard && hotelDashboard.style.display !== 'none') {
        // Load hotel menu items
        fetch('/my-menu')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    displayHotelMenu(data.menu_items);
                }
            })
            .catch(error => console.error('Error loading hotel menu:', error));
        
        // Load hotel stats
        loadMenuStats();
    } else {
        // Load student dashboard
        fetch('/my-posts')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    displayUserReviews(data.reviews);
                    displayUserFoods(data.food_posts);
                }
            })
            .catch(error => console.error('Error loading dashboard:', error));
    }
}

// Display user reviews
function displayUserReviews(reviews) {
    const container = document.getElementById('userReviews');
    if (reviews.length === 0) {
        container.innerHTML = '<p class="no-content">No reviews yet. Post your first review!</p>';
        return;
    }
    
    container.innerHTML = reviews.map(review => `
        <div class="dashboard-post">
            <div class="post-header">
                <h4>${review.restaurant} - ${review.menu_item}</h4>
                <span class="rating">${'⭐'.repeat(review.rating)}</span>
            </div>
            <p>${review.comment}</p>
            <small class="post-time">${review.timeAgo}</small>
        </div>
    `).join('');
}

// Display user food posts
function displayUserFoods(foods) {
    const container = document.getElementById('userFoods');
    if (foods.length === 0) {
        container.innerHTML = '<p class="no-content">No food posts yet. Share your homemade delicacies!</p>';
        return;
    }
    
    container.innerHTML = foods.map(food => `
        <div class="dashboard-post">
            <div class="post-header">
                <h4>${food.title}</h4>
                <span class="price">৳${food.price}</span>
                <span class="status ${food.is_available ? 'available' : 'unavailable'}">
                    ${food.is_available ? 'Available' : 'Sold Out'}
                </span>
            </div>
            <p>${food.description}</p>
            <div class="post-details">
                <span>📍 ${food.location}</span>
                <span>📞 ${food.contact_info}</span>
            </div>
            <small class="post-time">${food.timeAgo}</small>
        </div>
    `).join('');
}

// Display hotel menu items
function displayHotelMenu(menuItems) {
    const container = document.getElementById('hotelMenu');
    if (menuItems.length === 0) {
        container.innerHTML = '<p class="no-content">No menu items yet. Add your first dish!</p>';
        return;
    }
    
    container.innerHTML = menuItems.map(item => {
        const timeRemaining = item.time_remaining || '0:00:00';
        const isExpired = item.is_expired || false;
        const hoursLeft = timeRemaining.split(':')[0];
        const minutesLeft = timeRemaining.split(':')[1];
        
        return `
        <div class="dashboard-post menu-item-card ${isExpired ? 'expired' : ''}" data-item-id="${item.id}">
            <div class="post-header">
                <div class="menu-item-info">
                    <h4>${item.item_name}</h4>
                    <span class="price">৳${item.price}</span>
                </div>
                <div class="menu-item-controls">
                    <button class="btn btn-sm ${item.is_available ? 'btn-success' : 'btn-warning'}" 
                            onclick="toggleMenuAvailability(${item.id})" 
                            title="${item.is_available ? 'Mark as Unavailable' : 'Mark as Available'}">
                        ${item.is_available ? '✓ Available' : '⚠ Unavailable'}
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteMenuItem(${item.id})" title="Delete Item">
                        🗑️
                    </button>
                </div>
            </div>
            <p class="menu-description">${item.description}</p>
            <div class="post-details">
                <span class="category-tag">🍽️ ${item.category}</span>
                <span class="rating-info">⭐ ${item.average_rating || 0}/5 (${item.review_count || 0} reviews)</span>
            </div>
            <div class="time-info">
                <small class="post-time">Added ${item.created_at ? new Date(item.created_at).toLocaleDateString() : 'recently'}</small>
                <small class="expiry-time ${isExpired ? 'expired' : (hoursLeft < 2 ? 'expiring-soon' : '')}">
                    ${isExpired ? '⏰ Expired' : `⏰ ${hoursLeft}h ${minutesLeft}m left`}
                </small>
            </div>
        </div>
    `;
    }).join('');
}

// Load restaurants for review form
function loadRestaurants() {
    fetch('/api/hotels')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('restaurantSelect');
            select.innerHTML = '<option value="">Select a restaurant</option>';
            data.forEach(hotel => {
                select.innerHTML += `<option value="${hotel.id}">${hotel.name}</option>`;
            });
        })
        .catch(error => console.error('Error loading restaurants:', error));
}

// Load menu items based on selected restaurant
function loadMenuItems() {
    const restaurantId = document.getElementById('restaurantSelect').value;
    const menuSelect = document.getElementById('menuItemSelect');
    
    if (!restaurantId) {
        menuSelect.innerHTML = '<option value="">Select restaurant first</option>';
        return;
    }
    
    // This would need to be implemented as a new API endpoint
    fetch(`/api/menu-items/${restaurantId}`)
        .then(response => response.json())
        .then(data => {
            menuSelect.innerHTML = '<option value="">Select a menu item</option>';
            data.forEach(item => {
                menuSelect.innerHTML += `<option value="${item.id}">${item.item_name} - ৳${item.price}</option>`;
            });
        })
        .catch(error => {
            console.error('Error loading menu items:', error);
            menuSelect.innerHTML = '<option value="">Error loading items</option>';
        });
}

// Form submission handlers for new features
document.addEventListener('DOMContentLoaded', function() {
    // Review form submission
    const reviewForm = document.getElementById('reviewForm');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/post-review', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Review posted successfully!');
                    closeModal('postReviewModal');
                    this.reset();
                    // Refresh the page to show new review
                    window.location.reload();
                } else {
                    alert(data.message || 'Failed to post review');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while posting review');
            });
        });
    }

    // Food form submission
    const foodForm = document.getElementById('foodForm');
    if (foodForm) {
        foodForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/post-food', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Food post created successfully!');
                    closeModal('postFoodModal');
                    this.reset();
                    // Refresh the page to show new post
                    window.location.reload();
                } else {
                    alert(data.message || 'Failed to post food');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while posting food');
            });
        });
    }

    // Menu form submission
    const menuForm = document.getElementById('menuForm');
    if (menuForm) {
        menuForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Menu form submitted');
            
            const formData = new FormData(this);
            console.log('Form data:', Object.fromEntries(formData));
            
            fetch('/add-menu-item', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                console.log('Response status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data);
                if (data.success) {
                    alert('Menu item added successfully!');
                    closeModal('addMenuModal');
                    this.reset();
                    // Refresh dashboard content
                    loadDashboardContent();
                } else {
                    alert(data.message || 'Failed to add menu item');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while adding menu item');
            });
        });
    } else {
        console.log('Menu form not found');
    }
    
    // Profile form submission
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/update-profile', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Profile updated successfully!');
                    closeModal('settingsModal');
                } else {
                    alert(data.message || 'Failed to update profile');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while updating profile');
            });
        });
    }

    // Password form submission
    const passwordForm = document.getElementById('passwordForm');
    if (passwordForm) {
        passwordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/change-password', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Password changed successfully!');
                    this.reset();
                    closeModal('settingsModal');
                } else {
                    alert(data.message || 'Failed to change password');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while changing password');
            });
        });
    }

    // Business form submission
    const businessForm = document.getElementById('businessForm');
    if (businessForm) {
        businessForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/update-business', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Business information updated successfully!');
                    closeModal('hotelSettingsModal');
                } else {
                    alert(data.message || 'Failed to update business information');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while updating business information');
            });
        });
    }

    // Hotel password form submission
    const hotelPasswordForm = document.getElementById('hotelPasswordForm');
    if (hotelPasswordForm) {
        hotelPasswordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/change-hotel-password', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Password changed successfully!');
                    this.reset();
                    closeModal('hotelSettingsModal');
                } else {
                    alert(data.message || 'Failed to change password');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while changing password');
            });
        });
    }
});
