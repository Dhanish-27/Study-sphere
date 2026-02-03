// EduHub Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validations
    initializeFormValidations();
    
    // Initialize AJAX handlers
    initializeAjaxHandlers();
    
    // Initialize mobile menu
    initializeMobileMenu();
});

// Mobile menu toggle
function initializeMobileMenu() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

// Form validation
function initializeFormValidations() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'This field is required');
            isValid = false;
        } else {
            clearFieldError(field);
        }
        
        // Email validation
        if (field.type === 'email' && field.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                showFieldError(field, 'Please enter a valid email address');
                isValid = false;
            }
        }
    });
    
    return isValid;
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'text-red-500 text-sm mt-1 field-error';
    errorDiv.textContent = message;
    
    field.classList.add('border-red-500');
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('border-red-500');
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
}

// AJAX handlers
function initializeAjaxHandlers() {
    // Like functionality
    document.addEventListener('click', function(e) {
        if (e.target.closest('[data-like-url]')) {
            e.preventDefault();
            const button = e.target.closest('[data-like-url]');
            const url = button.dataset.likeUrl;
            toggleLike(url, button);
        }
        
        // Follow functionality
        if (e.target.closest('[data-follow-url]')) {
            e.preventDefault();
            const button = e.target.closest('[data-follow-url]');
            const url = button.dataset.followUrl;
            toggleFollow(url, button);
        }
        
        // Save functionality
        if (e.target.closest('[data-save-url]')) {
            e.preventDefault();
            const button = e.target.closest('[data-save-url]');
            const url = button.dataset.saveUrl;
            toggleSave(url, button);
        }
    });
}

function toggleLike(url, button) {
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateLikeButton(button, data.liked, data.count);
        } else {
            showAlert(data.message || 'Error occurred', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Network error occurred', 'error');
    });
}

function toggleFollow(url, button) {
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateFollowButton(button, data.following);
        } else {
            showAlert(data.message || 'Error occurred', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Network error occurred', 'error');
    });
}

function toggleSave(url, button) {
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateSaveButton(button, data.saved);
        } else {
            showAlert(data.message || 'Error occurred', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Network error occurred', 'error');
    });
}

function updateLikeButton(button, liked, count) {
    const icon = button.querySelector('.material-symbols-outlined');
    const text = button.querySelector('span:not(.material-symbols-outlined)');
    
    if (liked) {
        icon.textContent = 'thumb_up';
        button.classList.add('text-primary-600');
    } else {
        icon.textContent = 'thumb_up_off_alt';
        button.classList.remove('text-primary-600');
    }
    
    if (text) {
        text.textContent = `Like (${count})`;
    }
}

function updateFollowButton(button, following) {
    const text = button.querySelector('span:not(.material-symbols-outlined)');
    
    if (following) {
        button.textContent = 'Following';
        button.classList.add('bg-gray-200', 'text-gray-700');
    } else {
        button.textContent = 'Follow';
        button.classList.remove('bg-gray-200', 'text-gray-700');
    }
}

function updateSaveButton(button, saved) {
    const icon = button.querySelector('.material-symbols-outlined');
    
    if (saved) {
        icon.textContent = 'bookmark';
        button.classList.add('text-primary-600');
    } else {
        icon.textContent = 'bookmark_border';
        button.classList.remove('text-primary-600');
    }
}

// Utility functions
function getCookie(name) {
    let cookieValue = null;
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

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} fade-in`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function showLoadingSpinner(button) {
    const originalContent = button.innerHTML;
    button.innerHTML = '<span class="spinner"></span> Loading...';
    button.disabled = true;
    
    return () => {
        button.innerHTML = originalContent;
        button.disabled = false;
    };
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (searchInput && searchResults) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length < 2) {
                searchResults.innerHTML = '';
                searchResults.classList.add('hidden');
                return;
            }
            
            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 300);
        });
        
        // Close search results when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.classList.add('hidden');
            }
        });
    }
}

function performSearch(query) {
    const url = `/search/?q=${encodeURIComponent(query)}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data);
        })
        .catch(error => {
            console.error('Search error:', error);
        });
}

function displaySearchResults(results) {
    const searchResults = document.getElementById('search-results');
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="p-4 text-gray-500">No results found</div>';
    } else {
        const html = results.map(result => `
            <a href="${result.url}" class="block p-3 hover:bg-gray-50 transition-colors">
                <div class="font-medium">${result.title}</div>
                <div class="text-sm text-gray-500">${result.type}</div>
            </a>
        `).join('');
        
        searchResults.innerHTML = html;
    }
    
    searchResults.classList.remove('hidden');
}

// Image preview
function initializeImagePreview() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    showImagePreview(e.target.result);
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

function showImagePreview(src) {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="max-w-4xl max-h-screen p-4">
            <img src="${src}" class="max-w-full max-h-full rounded-lg">
            <button class="absolute top-4 right-4 text-white bg-black bg-opacity-50 rounded-full p-2">
                <span class="material-symbols-outlined">close</span>
            </button>
        </div>
    `;
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal || e.target.closest('button')) {
            modal.remove();
        }
    });
    
    document.body.appendChild(modal);
}

// Tab functionality
function initializeTabs() {
    const tabButtons = document.querySelectorAll('[data-tab]');
    const tabContents = document.querySelectorAll('[data-tab-content]');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.dataset.tab;
            
            // Hide all tab contents
            tabContents.forEach(content => {
                content.classList.add('hidden');
            });
            
            // Remove active class from all buttons
            tabButtons.forEach(btn => {
                btn.classList.remove('active', 'bg-primary-100', 'text-primary-700');
            });
            
            // Show target tab content
            const targetContent = document.querySelector(`[data-tab-content="${targetTab}"]`);
            if (targetContent) {
                targetContent.classList.remove('hidden');
            }
            
            // Add active class to clicked button
            this.classList.add('active', 'bg-primary-100', 'text-primary-700');
        });
    });
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'absolute bg-gray-800 text-white text-xs rounded px-2 py-1 z-50';
            tooltip.textContent = this.dataset.tooltip;
            tooltip.style.bottom = '100%';
            tooltip.style.left = '50%';
            tooltip.style.transform = 'translateX(-50%) translateY(-4px)';
            
            this.style.position = 'relative';
            this.appendChild(tooltip);
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.absolute');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
}

// Export functions for use in other scripts
window.EduHub = {
    showAlert,
    showLoadingSpinner,
    getCookie,
    toggleLike,
    toggleFollow,
    toggleSave,
    validateForm
};
