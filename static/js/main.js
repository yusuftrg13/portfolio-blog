// Main JavaScript for Portfolio Blog

document.addEventListener('DOMContentLoaded', function() {
    // Theme management
    initTheme();
    
    // Navigation
    initNavigation();
    
    // Back to top button
    initBackToTop();
    
    // Search functionality
    initSearch();
    
    // Forms
    initForms();
    
    // Animations
    initAnimations();
});

// Theme Management
function initTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIconLight = document.getElementById('theme-icon-light');
    const themeIconDark = document.getElementById('theme-icon-dark');
    
    function updateThemeIcon() {
        const isDark = document.documentElement.classList.contains('dark');
        if (isDark) {
            themeIconLight.classList.remove('hidden');
            themeIconDark.classList.add('hidden');
        } else {
            themeIconLight.classList.add('hidden');
            themeIconDark.classList.remove('hidden');
        }
    }
    
    function setTheme(theme) {
        localStorage.setItem('theme', theme);
        
        if (theme === 'auto') {
            const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
            document.documentElement.classList.toggle('dark', systemTheme === 'dark');
        } else {
            document.documentElement.classList.toggle('dark', theme === 'dark');
        }
        
        updateThemeIcon();
    }
    
    // Theme toggle click handler
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = localStorage.getItem('theme') || 'auto';
            let nextTheme;
            
            switch (currentTheme) {
                case 'light':
                    nextTheme = 'dark';
                    break;
                case 'dark':
                    nextTheme = 'auto';
                    break;
                default:
                    nextTheme = 'light';
                    break;
            }
            
            setTheme(nextTheme);
        });
    }
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (localStorage.getItem('theme') === 'auto') {
            document.documentElement.classList.toggle('dark', e.matches);
            updateThemeIcon();
        }
    });
    
    // Initialize theme icon
    updateThemeIcon();
}

// Navigation
function initNavigation() {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Language menu toggle
    const languageToggle = document.getElementById('language-toggle');
    const languageMenu = document.getElementById('language-menu');
    
    if (languageToggle && languageMenu) {
        languageToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            languageMenu.classList.toggle('hidden');
        });
        
        // Close language menu when clicking outside
        document.addEventListener('click', function() {
            languageMenu.classList.add('hidden');
        });
        
        languageMenu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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
}

// Back to top button
function initBackToTop() {
    const backToTopButton = document.createElement('button');
    backToTopButton.className = 'back-to-top no-print';
    backToTopButton.innerHTML = `
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path>
        </svg>
    `;
    backToTopButton.setAttribute('aria-label', 'Back to top');
    document.body.appendChild(backToTopButton);
    
    // Show/hide button based on scroll position
    function toggleBackToTopButton() {
        if (window.scrollY > 300) {
            backToTopButton.classList.add('visible');
        } else {
            backToTopButton.classList.remove('visible');
        }
    }
    
    window.addEventListener('scroll', toggleBackToTopButton);
    
    // Scroll to top when clicked
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Search functionality
function initSearch() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    const searchResults = document.querySelector('.search-results');
    
    if (searchForm && searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length < 2) {
                if (searchResults) {
                    searchResults.innerHTML = '';
                    searchResults.classList.add('hidden');
                }
                return;
            }
            
            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 300);
        });
        
        // Close search results when clicking outside
        document.addEventListener('click', function(e) {
            if (searchResults && !searchForm.contains(e.target)) {
                searchResults.classList.add('hidden');
            }
        });
    }
}

async function performSearch(query) {
    const searchResults = document.querySelector('.search-results');
    if (!searchResults) return;
    
    try {
        const response = await fetch(`/search/?q=${encodeURIComponent(query)}&ajax=1`);
        const data = await response.json();
        
        searchResults.innerHTML = '';
        
        if (data.results && data.results.length > 0) {
            data.results.forEach(result => {
                const resultElement = document.createElement('a');
                resultElement.href = result.url;
                resultElement.className = 'block p-3 hover:bg-gray-100 dark:hover:bg-gray-700 border-b border-gray-200 dark:border-gray-600';
                resultElement.innerHTML = `
                    <div class="font-medium text-gray-900 dark:text-white">${result.title}</div>
                    <div class="text-sm text-gray-600 dark:text-gray-400">${result.summary}</div>
                `;
                searchResults.appendChild(resultElement);
            });
        } else {
            searchResults.innerHTML = '<div class="p-3 text-gray-600 dark:text-gray-400">No results found</div>';
        }
        
        searchResults.classList.remove('hidden');
    } catch (error) {
        console.error('Search error:', error);
    }
}

// Forms
function initForms() {
    // Comment form
    const commentForm = document.querySelector('.comment-form');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner"></span> Submitting...';
            }
        });
    }
    
    // Contact form
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner"></span> Sending...';
            }
        });
    }
    
    // Newsletter form
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    newsletterForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const submitButton = this.querySelector('button[type="submit"]');
            
            if (!emailInput.value.trim()) return;
            
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner"></span> Subscribing...';
            }
            
            try {
                const formData = new FormData(this);
                const response = await fetch(this.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showMessage('Thank you for subscribing!', 'success');
                    emailInput.value = '';
                } else {
                    showMessage(data.message || 'Subscription failed. Please try again.', 'error');
                }
            } catch (error) {
                showMessage('Network error. Please try again.', 'error');
            } finally {
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.innerHTML = 'Subscribe';
                }
            }
        });
    });
}

// Show message function
function showMessage(message, type = 'info') {
    const messageElement = document.createElement('div');
    messageElement.className = `alert alert-${type} fixed top-4 right-4 z-50 max-w-sm shadow-lg`;
    messageElement.innerHTML = `
        <div class="flex items-center justify-between">
            <span>${message}</span>
            <button class="ml-4 text-lg leading-none" onclick="this.parentElement.parentElement.remove()">&times;</button>
        </div>
    `;
    
    document.body.appendChild(messageElement);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (messageElement.parentElement) {
            messageElement.remove();
        }
    }, 5000);
}

// Animations
function initAnimations() {
    // Fade in on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements with fade-on-scroll class
    document.querySelectorAll('.fade-on-scroll').forEach(element => {
        observer.observe(element);
    });
    
    // Skill progress bars animation
    const skillBars = document.querySelectorAll('.skill-progress-bar');
    const skillObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const percentage = bar.dataset.percentage;
                bar.style.width = percentage + '%';
                skillObserver.unobserve(bar);
            }
        });
    }, { threshold: 0.5 });
    
    skillBars.forEach(bar => {
        bar.style.width = '0%';
        skillObserver.observe(bar);
    });
}

// Utility functions
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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Copy to clipboard function
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showMessage('Copied to clipboard!', 'success');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showMessage('Copied to clipboard!', 'success');
    }
}

// Share function
function sharePost(title, url) {
    if (navigator.share) {
        navigator.share({
            title: title,
            url: url
        }).catch(console.error);
    } else {
        copyToClipboard(url);
    }
}

// Print function
function printPage() {
    window.print();
}

// Load more functionality for infinite scroll
function loadMore(url, container, button) {
    button.disabled = true;
    button.innerHTML = '<span class="spinner"></span> Loading...';
    
    fetch(url)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newItems = doc.querySelectorAll('.load-more-item');
            
            newItems.forEach(item => {
                container.appendChild(item);
            });
            
            const nextButton = doc.querySelector('.load-more-btn');
            if (nextButton) {
                button.onclick = () => loadMore(nextButton.dataset.url, container, button);
                button.disabled = false;
                button.innerHTML = 'Load More';
            } else {
                button.remove();
            }
        })
        .catch(error => {
            console.error('Error loading more:', error);
            button.disabled = false;
            button.innerHTML = 'Try Again';
        });
}