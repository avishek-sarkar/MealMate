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
            
            const formData = new FormData(this);
            formData.append('user_type', 'hotel');
            
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
    console.log('Liked post:', postId);
}

function commentPost(postId) {
    // Add comment functionality
    console.log('Comment on post:', postId);
}

function sharePost(postId) {
    // Add share functionality
    console.log('Share post:', postId);
}
