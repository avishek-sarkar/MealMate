// Admin Panel JavaScript

// Common functions for all admin pages
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-refresh dashboard every 5 minutes
    if (window.location.pathname === '/admin/dashboard') {
        setInterval(refreshDashboardStats, 300000);
    }
});

// Refresh dashboard statistics
async function refreshDashboardStats() {
    try {
        const response = await fetch('/admin/dashboard');
        if (response.ok) {
            // Reload the page to get updated stats
            window.location.reload();
        }
    } catch (error) {
        console.log('Failed to refresh dashboard stats');
    }
}

// Common message display function
function showMessage(message, type = 'success') {
    // Create alert if it doesn't exist
    let alert = document.getElementById('messageAlert');
    if (!alert) {
        alert = document.createElement('div');
        alert.id = 'messageAlert';
        alert.className = 'alert alert-dismissible fade show position-fixed top-0 end-0 m-3';
        alert.style.zIndex = '9999';
        alert.innerHTML = `
            <span id="messageText"></span>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alert);
    }
    
    const messageText = document.getElementById('messageText');
    
    alert.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    alert.style.zIndex = '9999';
    messageText.textContent = message;
    alert.classList.remove('d-none');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (alert && !alert.classList.contains('d-none')) {
            alert.classList.add('d-none');
        }
    }, 5000);
}

// Confirm action with custom message
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Loading state for buttons
function setButtonLoading(button, loading = true) {
    if (loading) {
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    } else {
        button.disabled = false;
        button.innerHTML = button.getAttribute('data-original-text') || 'Action';
    }
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Handle AJAX form submissions
function handleFormSubmit(form, url, method = 'POST') {
    return new Promise(async (resolve, reject) => {
        try {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                resolve(result);
            } else {
                reject(new Error(result.message || 'Operation failed'));
            }
        } catch (error) {
            reject(error);
        }
    });
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Search functionality
function initializeSearch(searchInputId, tableId) {
    const searchInput = document.getElementById(searchInputId);
    const table = document.getElementById(tableId);
    
    if (!searchInput || !table) return;
    
    const debouncedSearch = debounce(function(searchTerm) {
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(searchTerm.toLowerCase())) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }, 300);
    
    searchInput.addEventListener('input', function() {
        debouncedSearch(this.value);
    });
}

// Export data functionality
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const row = [], cols = rows[i].querySelectorAll('td, th');
        
        for (let j = 0; j < cols.length - 1; j++) { // Exclude actions column
            let cellText = cols[j].innerText.replace(/"/g, '""');
            row.push('"' + cellText + '"');
        }
        
        csv.push(row.join(','));
    }
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename + '.csv';
    a.click();
    
    window.URL.revokeObjectURL(url);
}

// Theme switcher (if needed)
function toggleTheme() {
    const body = document.body;
    body.classList.toggle('dark-theme');
    
    const isDark = body.classList.contains('dark-theme');
    localStorage.setItem('admin-theme', isDark ? 'dark' : 'light');
}

// Load saved theme
function loadTheme() {
    const savedTheme = localStorage.getItem('admin-theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
}

// Initialize theme on page load
loadTheme();
