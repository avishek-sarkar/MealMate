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

// View Hotel Menu functionality
async function viewHotelMenu(hotelId, hotelName) {
    const modal = document.getElementById('viewMenuModal');
    const modalTitle = document.getElementById('menuModalTitle');
    const loadingMessage = document.getElementById('menuLoadingMessage');
    const menuContent = document.getElementById('menuContent');
    const menuGrid = document.getElementById('menuGrid');
    const noMenuMessage = document.getElementById('noMenuMessage');
    
    // Set hotel name in modal title
    modalTitle.textContent = `${hotelName} - Menu`;
    
    // Show modal
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // Show loading state
    loadingMessage.style.display = 'block';
    menuContent.style.display = 'none';
    
    try {
        // Fetch menu items
        const response = await fetch(`/api/menu-items/${hotelId}`);
        const menuItems = await response.json();
        
        // Hide loading message
        loadingMessage.style.display = 'none';
        menuContent.style.display = 'block';
        
        if (menuItems && menuItems.length > 0) {
            // Display menu items
            menuGrid.innerHTML = '';
            noMenuMessage.style.display = 'none';
            
            menuItems.forEach(item => {
                const menuCard = createMenuCard(item);
                menuGrid.appendChild(menuCard);
            });
        } else {
            // Show no menu message
            menuGrid.innerHTML = '';
            noMenuMessage.style.display = 'block';
        }
        
    } catch (error) {
        console.error('Error fetching menu:', error);
        loadingMessage.style.display = 'none';
        menuContent.style.display = 'block';
        menuGrid.innerHTML = '<p class="text-center" style="color: #666; padding: 20px;">Failed to load menu. Please try again.</p>';
        noMenuMessage.style.display = 'none';
    }
}

// Create menu card element
function createMenuCard(item) {
    const card = document.createElement('div');
    card.className = 'menu-item-card';
    
    const imageUrl = item.image_url || 'https://via.placeholder.com/200x150?text=Food+Item';
    
    card.innerHTML = `
        <div class="menu-item-image">
            <img src="${imageUrl}" alt="${item.item_name}" onerror="this.src='https://via.placeholder.com/200x150?text=Food+Item'">
        </div>
        <div class="menu-item-info">
            <h4 class="menu-item-name">${item.item_name}</h4>
            <p class="menu-item-description">${item.description || 'No description available'}</p>
            <div class="menu-item-details">
                <span class="menu-item-price">৳${item.price}</span>
                <span class="menu-item-category">${item.category}</span>
            </div>
            <div class="menu-item-meta">
                <span class="menu-item-availability ${item.is_available ? 'available' : 'unavailable'}">
                    ${item.is_available ? '● Available' : '● Unavailable'}
                </span>
            </div>
        </div>
    `;
    
    return card;
}

// ============================================================================
// REAL-TIME NOTIFICATIONS & POST INTERACTIONS
// ============================================================================

// Socket.IO connection
let socket = null;
let notificationsPanel = null;

// Initialize real-time features
document.addEventListener('DOMContentLoaded', function() {
    initializeRealTimeFeatures();
    initializePostInteractions();
    loadPostInteractions();
});

function initializeRealTimeFeatures() {
    // Check if user is logged in (you can set this from the server)
    const isLoggedIn = document.querySelector('.user-menu') !== null;
    
    if (isLoggedIn && typeof io !== 'undefined') {
        // Initialize Socket.IO connection
        socket = io();
        
        socket.on('connect', function() {
            console.log('Connected to real-time notifications');
        });
        
        socket.on('new_notification', function(notification) {
            showNotificationToast(notification);
            updateNotificationCount();
        });
        
        socket.on('new_post', function(data) {
            showNewPostNotification(data);
            addNewPostToFeed(data);
        });
        
        socket.on('disconnect', function() {
            console.log('Disconnected from notifications');
        });
        
        // Load initial notification count
        updateNotificationCount();
    }
    
    notificationsPanel = document.getElementById('notificationsPanel');
}

function initializePostInteractions() {
    // Like button handlers
    document.addEventListener('click', function(e) {
        if (e.target.closest('.like-btn')) {
            e.preventDefault();
            handleLikeClick(e.target.closest('.like-btn'));
        }
        
        if (e.target.closest('.comment-btn')) {
            e.preventDefault();
            handleCommentClick(e.target.closest('.comment-btn'));
        }
    });
    
    // Comment form handler
    const commentForm = document.getElementById('commentForm');
    if (commentForm) {
        commentForm.addEventListener('submit', handleCommentSubmit);
    }
    
    // Character counter for comment textarea
    const commentText = document.getElementById('commentText');
    if (commentText) {
        commentText.addEventListener('input', updateCharacterCount);
    }
}

function loadPostInteractions() {
    // Load interaction counts for all posts
    const postCards = document.querySelectorAll('.post-card');
    postCards.forEach(card => {
        const likeBtn = card.querySelector('.like-btn');
        const commentBtn = card.querySelector('.comment-btn');
        
        if (likeBtn && commentBtn) {
            const postId = likeBtn.dataset.postId;
            const postType = likeBtn.dataset.postType;
            
            fetch(`/api/post/interactions/${postId}/${postType}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        updateInteractionCounts(card, data);
                    }
                })
                .catch(error => console.error('Error loading interactions:', error));
        }
    });
}

function handleLikeClick(button) {
    const postId = button.dataset.postId;
    const postType = button.dataset.postType;
    
    if (!postId || !postType) return;
    
    fetch('/api/post/like', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            post_id: parseInt(postId),
            post_type: postType
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateLikeButton(button, data);
        } else {
            if (data.message === 'Login required') {
                showLoginModal();
            } else {
                showNotification(data.message, 'error');
            }
        }
    })
    .catch(error => {
        console.error('Error handling like:', error);
        showNotification('Failed to process like', 'error');
    });
}

function handleCommentClick(button) {
    const postId = button.dataset.postId;
    const postType = button.dataset.postType;
    
    // Check if user is logged in
    const isLoggedIn = document.querySelector('.user-menu') !== null;
    if (!isLoggedIn) {
        showLoginModal();
        return;
    }
    
    // Show comment modal
    document.getElementById('commentPostId').value = postId;
    document.getElementById('commentPostType').value = postType;
    document.getElementById('commentModal').style.display = 'block';
    document.getElementById('commentText').focus();
}

function handleCommentSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        post_id: parseInt(formData.get('post_id')),
        post_type: formData.get('post_type'),
        comment_text: formData.get('comment_text').trim()
    };
    
    if (!data.comment_text) {
        showNotification('Please enter a comment', 'error');
        return;
    }
    
    fetch('/api/post/comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            closeCommentModal();
            showNotification('Comment added successfully!', 'success');
            updateCommentsCount(data.post_id, data.post_type, result.comments_count);
        } else {
            showNotification(result.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error adding comment:', error);
        showNotification('Failed to add comment', 'error');
    });
}

function updateLikeButton(button, data) {
    const icon = button.querySelector('i');
    const countSpan = button.querySelector('.likes-count');
    
    if (data.user_has_liked) {
        icon.className = 'fas fa-heart';
        button.classList.add('liked');
    } else {
        icon.className = 'far fa-heart';
        button.classList.remove('liked');
    }
    
    countSpan.textContent = data.likes_count;
}

function updateCommentsCount(postId, postType, count) {
    const postCard = document.querySelector(`[data-post-id="${postId}"][data-post-type="${postType}"]`).closest('.post-card');
    const commentBtn = postCard.querySelector('.comment-btn .comments-count');
    if (commentBtn) {
        commentBtn.textContent = count;
    }
}

function updateInteractionCounts(card, data) {
    const likeBtn = card.querySelector('.like-btn');
    const commentBtn = card.querySelector('.comment-btn');
    
    if (likeBtn) {
        const icon = likeBtn.querySelector('i');
        const countSpan = likeBtn.querySelector('.likes-count');
        
        countSpan.textContent = data.likes_count;
        
        if (data.user_has_liked) {
            icon.className = 'fas fa-heart';
            likeBtn.classList.add('liked');
        } else {
            icon.className = 'far fa-heart';
            likeBtn.classList.remove('liked');
        }
    }
    
    if (commentBtn) {
        const countSpan = commentBtn.querySelector('.comments-count');
        countSpan.textContent = data.comments_count;
    }
}

function updateCharacterCount() {
    const textarea = document.getElementById('commentText');
    const counter = document.querySelector('.character-count');
    if (textarea && counter) {
        const current = textarea.value.length;
        const max = 500;
        counter.textContent = `${current}/${max}`;
        
        if (current > max) {
            counter.style.color = '#dc3545';
        } else if (current > max * 0.9) {
            counter.style.color = '#ffc107';
        } else {
            counter.style.color = '#666';
        }
    }
}

function closeCommentModal() {
    document.getElementById('commentModal').style.display = 'none';
    document.getElementById('commentForm').reset();
    updateCharacterCount();
}

// Notification functions
function toggleNotifications() {
    if (notificationsPanel.style.display === 'none' || !notificationsPanel.style.display) {
        loadNotifications();
        notificationsPanel.style.display = 'block';
    } else {
        notificationsPanel.style.display = 'none';
    }
}

function loadNotifications() {
    const content = document.getElementById('notificationsContent');
    content.innerHTML = '<div class="loading-notifications"><i class="fas fa-spinner fa-spin"></i> Loading notifications...</div>';
    
    fetch('/api/notifications')
        .then(response => {
            console.log('Load notifications response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Load notifications response:', data);
            if (data.success) {
                displayNotifications(data.notifications);
            } else {
                content.innerHTML = `<div class="no-notifications">${data.message || 'Failed to load notifications'}</div>`;
            }
        })
        .catch(error => {
            console.error('Error loading notifications:', error);
            content.innerHTML = '<div class="no-notifications">Failed to load notifications</div>';
        });
}

function displayNotifications(notifications) {
    const content = document.getElementById('notificationsContent');
    
    if (notifications.length === 0) {
        content.innerHTML = '<div class="no-notifications"><i class="fas fa-bell-slash"></i><br>No notifications yet</div>';
        return;
    }
    
    const notificationsHtml = notifications.map(notification => `
        <div class="notification-item ${notification.is_read ? '' : 'unread'}" onclick="markNotificationAsRead(${notification.id})">
            <div class="notification-title">${notification.title}</div>
            <div class="notification-message">${notification.message}</div>
            <div class="notification-time">${notification.time_ago}</div>
        </div>
    `).join('');
    
    content.innerHTML = notificationsHtml;
}

function updateNotificationCount() {
    fetch('/api/notifications')
        .then(response => {
            console.log('Notifications API response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Notifications API response:', data);
            if (data.success) {
                const countElement = document.getElementById('notificationCount');
                if (countElement) {
                    if (data.unread_count > 0) {
                        countElement.textContent = data.unread_count;
                        countElement.style.display = 'block';
                    } else {
                        countElement.style.display = 'none';
                    }
                }
            } else {
                console.log('Notifications API error:', data.message);
            }
        })
        .catch(error => {
            console.error('Error updating notification count:', error);
        });
}

function markNotificationAsRead(notificationId) {
    if (socket) {
        socket.emit('mark_notification_read', { notification_id: notificationId });
    }
    updateNotificationCount();
}

function showNotificationToast(notification) {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = 'notification-toast';
    toast.innerHTML = `
        <div class="toast-content">
            <strong>${notification.title}</strong>
            <p>${notification.message}</p>
        </div>
        <button class="close-toast" onclick="this.parentElement.remove()">×</button>
    `;
    
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

function showNewPostNotification(data) {
    const notification = document.createElement('div');
    notification.className = 'new-post-notification';
    notification.innerHTML = `
        <strong>New ${data.type} post!</strong>
        <button class="close-notification" onclick="this.parentElement.remove()">×</button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => notification.classList.add('show'), 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

function addNewPostToFeed(data) {
    // Add new post to the top of the feed
    const postsContainer = document.querySelector('.newsfeed');
    if (postsContainer && data.data) {
        const newPostHtml = createPostHtml(data.data);
        postsContainer.insertAdjacentHTML('afterbegin', newPostHtml);
        
        // Initialize interactions for the new post
        setTimeout(() => {
            const newPost = postsContainer.firstElementChild;
            if (newPost) {
                const likeBtn = newPost.querySelector('.like-btn');
                const commentBtn = newPost.querySelector('.comment-btn');
                
                if (likeBtn && commentBtn) {
                    const postId = likeBtn.dataset.postId;
                    const postType = likeBtn.dataset.postType;
                    
                    fetch(`/api/post/interactions/${postId}/${postType}`)
                        .then(response => response.json())
                        .then(interactionData => {
                            if (interactionData.success) {
                                updateInteractionCounts(newPost, interactionData);
                            }
                        })
                        .catch(error => console.error('Error loading interactions for new post:', error));
                }
            }
        }, 500);
    }
}

function createPostHtml(post) {
    return `
        <div class="post-card">
            <div class="post-header">
                <div class="post-info">
                    <h3>${post.user.name}</h3>
                    <span class="post-time">${post.timeAgo}</span>
                </div>
            </div>
            <div class="post-content">
                ${post.type === 'review' ? `
                    <div class="review-content">
                        <h4>${post.restaurant} - ${post.menuItem}</h4>
                        <div class="rating">
                            ${'⭐'.repeat(post.rating)}
                            <span class="price">৳${post.price}</span>
                        </div>
                        <p>${post.comment}</p>
                    </div>
                ` : `
                    <div class="homemade-content">
                        <h4>${post.title}</h4>
                        <p>${post.description}</p>
                        <div class="food-details">
                            <span class="price">৳${post.price}</span>
                            <span class="location">📍${post.location}</span>
                            ${post.isVegetarian ? '<span class="veg-tag">🌱 Vegetarian</span>' : ''}
                        </div>
                    </div>
                `}
                ${post.image ? `<img src="${post.image}" alt="Post image" class="post-image">` : ''}
            </div>
            <div class="post-actions">
                <button class="action-btn like-btn" data-post-id="${post.id}" data-post-type="${post.type}">
                    <i class="far fa-heart"></i> <span class="likes-count">0</span>
                </button>
                <button class="action-btn comment-btn" data-post-id="${post.id}" data-post-type="${post.type}">
                    <i class="fas fa-comment"></i> <span class="comments-count">0</span>
                </button>
                <button class="action-btn share-btn">
                    <i class="fas fa-share"></i> Share
                </button>
            </div>
        </div>
    `;
}

function showNotification(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `notification-toast ${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <p>${message}</p>
        </div>
        <button class="close-toast" onclick="this.parentElement.remove()">×</button>
    `;
    
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ============================================================================
// EVENT HANDLERS FOR MODALS
// ============================================================================

// Close comment modal when clicking outside
document.addEventListener('click', function(e) {
    const modal = document.getElementById('commentModal');
    if (e.target === modal) {
        closeCommentModal();
    }
});

// Close comment modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const modal = document.getElementById('commentModal');
        if (modal && modal.style.display === 'block') {
            closeCommentModal();
        }
    }
});

// Close notifications panel when clicking outside
document.addEventListener('click', function(e) {
    const panel = document.getElementById('notificationsPanel');
    const bell = document.querySelector('.notification-bell');
    
    if (panel && panel.style.display === 'block' && 
        !panel.contains(e.target) && !bell.contains(e.target)) {
        panel.style.display = 'none';
    }
});
