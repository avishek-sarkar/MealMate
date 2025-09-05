// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeNavigation();
    initializeFilters();
    initializeModal();
    initializeTimeCountdown();
    initializeSmoothScrolling();
    initializeFormHandling();
});

// Navigation functionality
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Get the target section
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                // Smooth scroll to section
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Filter functionality for posts
function initializeFilters() {
    const filterTabs = document.querySelectorAll('.filter-tab');
    const posts = document.querySelectorAll('.post-card');
    
    filterTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            filterTabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            const filterType = this.getAttribute('data-filter');
            
            // Filter posts
            posts.forEach(post => {
                const postType = post.getAttribute('data-type');
                
                if (filterType === 'all' || postType === filterType) {
                    post.style.display = 'block';
                    setTimeout(() => {
                        post.style.opacity = '1';
                        post.style.transform = 'translateY(0)';
                    }, 100);
                } else {
                    post.style.opacity = '0';
                    post.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        post.style.display = 'none';
                    }, 300);
                }
            });
        });
    });
}

// Modal functionality
function initializeModal() {
    const loginButtons = document.querySelectorAll('.btn-outline');
    const modal = document.getElementById('loginModal');
    const closeBtn = document.querySelector('.close');
    
    // Open modal when login button is clicked
    loginButtons.forEach(btn => {
        if (btn.textContent.trim() === 'Login') {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                modal.style.display = 'block';
                document.body.style.overflow = 'hidden';
            });
        }
    });
    
    // Close modal when X is clicked
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });
    }
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
}

// Time countdown functionality
function initializeTimeCountdown() {
    const timeElements = document.querySelectorAll('.time-remaining span, .time-badge span');
    
    // Simulate countdown for demo purposes
    timeElements.forEach(element => {
        const text = element.textContent;
        if (text.includes('hours') || text.includes('h left')) {
            updateCountdown(element);
        }
    });
}

function updateCountdown(element) {
    const text = element.textContent;
    let hours = parseInt(text.match(/\d+/)[0]);
    
    // Update every minute for demo (in real app, this would be more sophisticated)
    const interval = setInterval(() => {
        if (hours > 0) {
            hours--;
            if (text.includes('Expires in')) {
                element.textContent = `Expires in ${hours} hours`;
            } else {
                element.textContent = `${hours}h left`;
            }
            
            // Change color as time decreases
            if (hours <= 2) {
                element.style.color = '#dc3545';
            } else if (hours <= 6) {
                element.style.color = '#ffc107';
            }
        } else {
            element.textContent = 'Expired';
            element.style.color = '#dc3545';
            clearInterval(interval);
        }
    }, 60000); // Update every minute
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Form handling - Flask integration
function initializeFormHandling() {
    // Forms are now handled by Flask server-side
    // Keep modal functionality for user experience
}

// Update UI for logged in user
function updateUIForLoggedInUser() {
    const navAuth = document.querySelector('.nav-auth');
    navAuth.innerHTML = `
        <div class="user-menu">
            <img src="https://via.placeholder.com/32x32" alt="User" class="user-avatar-small">
            <span>Welcome back!</span>
            <button class="btn btn-outline" onclick="logout()">Logout</button>
        </div>
    `;
    
    // Add styles for user menu
    const style = document.createElement('style');
    style.textContent = `
        .user-menu {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .user-avatar-small {
            width: 32px;
            height: 32px;
            border-radius: 50%;
        }
    `;
    document.head.appendChild(style);
}

// Logout function
function logout() {
    const navAuth = document.querySelector('.nav-auth');
    navAuth.innerHTML = `
        <button class="btn btn-outline">Login</button>
        <button class="btn btn-primary">Sign Up</button>
    `;
    
    // Re-initialize modal functionality
    initializeModal();
    
    alert('Logged out successfully!');
}

// Post interaction handlers
function initializePostInteractions() {
    // Like/reaction buttons
    const actionButtons = document.querySelectorAll('.action-btn');
    
    actionButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const icon = this.querySelector('i');
            const countSpan = this.querySelector('span') || this.childNodes[1];
            
            if (icon.classList.contains('fa-thumbs-up') || icon.classList.contains('fa-heart')) {
                // Toggle like state
                if (icon.classList.contains('fas')) {
                    icon.classList.remove('fas');
                    icon.classList.add('far');
                    this.style.color = '#666';
                    
                    // Decrease count
                    if (countSpan && countSpan.textContent) {
                        let count = parseInt(countSpan.textContent.trim()) - 1;
                        countSpan.textContent = ` ${count}`;
                    }
                } else {
                    icon.classList.remove('far');
                    icon.classList.add('fas');
                    this.style.color = '#ff6b35';
                    
                    // Increase count
                    if (countSpan && countSpan.textContent) {
                        let count = parseInt(countSpan.textContent.trim()) + 1;
                        countSpan.textContent = ` ${count}`;
                    }
                }
                
                // Add animation
                this.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 200);
            }
        });
    });
    
    // Contact seller buttons
    const contactButtons = document.querySelectorAll('.btn-primary');
    
    contactButtons.forEach(btn => {
        if (btn.textContent.includes('Contact')) {
            btn.addEventListener('click', function() {
                alert('Contact feature would open messaging system or phone dialer in a real app!');
            });
        }
    });
}

// Initialize post interactions when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializePostInteractions();
});

// Scroll-based animations
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe all cards and posts
    const animatedElements = document.querySelectorAll('.post-card, .hotel-card, .homemade-card');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Initialize scroll animations
document.addEventListener('DOMContentLoaded', function() {
    // Small delay to ensure all content is loaded
    setTimeout(initializeScrollAnimations, 500);
});

// Search functionality (if search is added later)
function initializeSearch() {
    const searchInput = document.querySelector('.search-input');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const posts = document.querySelectorAll('.post-card');
            const hotels = document.querySelectorAll('.hotel-card');
            const homemadeCards = document.querySelectorAll('.homemade-card');
            
            // Search through posts
            posts.forEach(post => {
                const content = post.textContent.toLowerCase();
                if (content.includes(searchTerm)) {
                    post.style.display = 'block';
                } else {
                    post.style.display = 'none';
                }
            });
            
            // Search through hotels
            hotels.forEach(hotel => {
                const content = hotel.textContent.toLowerCase();
                if (content.includes(searchTerm)) {
                    hotel.style.display = 'block';
                } else {
                    hotel.style.display = 'none';
                }
            });
            
            // Search through homemade food
            homemadeCards.forEach(card => {
                const content = card.textContent.toLowerCase();
                if (content.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

// Mobile menu toggle (for responsive design)
function initializeMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('nav-open');
        });
    }
}

// Initialize all features
document.addEventListener('DOMContentLoaded', function() {
    initializeMobileMenu();
    initializeSearch();
});

// Add some utility functions for future features
const MealMateUtils = {
    // Format time remaining
    formatTimeRemaining: function(hours) {
        if (hours <= 0) return 'Expired';
        if (hours < 1) return 'Less than 1 hour';
        return `${hours} hour${hours > 1 ? 's' : ''} left`;
    },
    
    // Generate random rating
    generateRating: function() {
        return (Math.random() * (5 - 3) + 3).toFixed(1);
    },
    
    // Format price
    formatPrice: function(price) {
        return `₹${price}`;
    },
    
    // Get time ago string
    getTimeAgo: function(hours) {
        if (hours < 1) return 'Just now';
        if (hours < 24) return `${Math.floor(hours)} hours ago`;
        const days = Math.floor(hours / 24);
        return `${days} day${days > 1 ? 's' : ''} ago`;
    }
};

// Export for potential use in other scripts
window.MealMateUtils = MealMateUtils;

// Flask-specific functions
function showLoginModal() {
    document.getElementById('loginModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function showRegisterModal() {
    hideModal('loginModal');
    document.getElementById('registerModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function hideModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Like post functionality with Flask backend
async function likePost(postId, button) {
    try {
        const response = await fetch(`/api/posts/${postId}/like`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action: 'like' })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const countSpan = button.querySelector('span');
            countSpan.textContent = data.likes;
            
            // Visual feedback
            button.style.transform = 'scale(1.2)';
            setTimeout(() => {
                button.style.transform = 'scale(1)';
            }, 200);
        } else {
            if (response.status === 401) {
                alert('Please login to like posts!');
                showLoginModal();
            } else {
                alert('Error liking post: ' + data.error);
            }
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error liking post. Please try again.');
    }
}

// Contact seller function
function contactSeller(sellerName) {
    alert(`Contact feature would open messaging system with ${sellerName} in a real app!`);
}

// View hotel menu function
function viewHotelMenu(hotelName) {
    alert(`View menu feature would show detailed menu for ${hotelName} in a real app!`);
}

// Post food function
function postFood() {
    alert('Post food feature would open a form to create new listing in a real app!');
}

// Sort homemade food
async function sortHomemadeFood(sortBy) {
    try {
        const response = await fetch(`/api/homemade-food?sort=${sortBy}`);
        const data = await response.json();
        
        // Update the homemade food grid
        updateHomemadeFoodGrid(data);
    } catch (error) {
        console.error('Error sorting food:', error);
    }
}

function updateHomemadeFoodGrid(foodItems) {
    const grid = document.querySelector('.homemade-grid');
    
    grid.innerHTML = foodItems.map(food => `
        <div class="homemade-card">
            <div class="card-image">
                <img src="${food.image}" alt="${food.title}">
                <div class="time-badge">
                    <i class="fas fa-clock"></i>
                    <span>${food.expiresIn}</span>
                </div>
            </div>
            <div class="card-content">
                <h3>${food.title}</h3>
                <div class="seller-info">
                    <img src="${food.seller.avatar}" alt="${food.seller.name}" class="seller-avatar">
                    <span>by ${food.seller.name}</span>
                </div>
                <p>${food.description}</p>
                <div class="food-specs">
                    ${food.isVegetarian ? 
                        '<span class="spec"><i class="fas fa-leaf"></i> Vegetarian</span>' : 
                        '<span class="spec"><i class="fas fa-drumstick-bite"></i> Non-Veg</span>'
                    }
                    <span class="spec"><i class="fas fa-users"></i> Serves ${food.servingSize}</span>
                </div>
                <div class="card-footer">
                    <div class="price">₹${food.price}</div>
                    <div class="location">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>${food.location}</span>
                    </div>
                </div>
                <button class="btn btn-primary full-width" onclick="contactSeller('${food.seller.name}')">
                    Contact Seller
                </button>
            </div>
        </div>
    `).join('');
}

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
});
