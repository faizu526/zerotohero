// ===== MOBILE RESPONSIVE & LOADING ANIMATIONS =====

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all modules
    initPageLoader();
    initMobileOptimizations();
    initSmoothScrolling();
    initFormLoading();
    initTouchFeedback();
    initRedirectLoading();
});

// ===== PAGE LOADER =====
function initPageLoader() {
    // Create loader element if it doesn't exist
    if (!document.querySelector('.page-loader')) {
        const loader = document.createElement('div');
        loader.className = 'page-loader';
        loader.innerHTML = `
            <div class="loader-spinner"></div>
            <div class="loader-text">Loading...</div>
        `;
        document.body.appendChild(loader);
    }

    // Hide loader when page is fully loaded
    window.addEventListener('load', function() {
        setTimeout(() => {
            const loader = document.querySelector('.page-loader');
            if (loader) {
                loader.classList.add('hidden');
                setTimeout(() => {
                    loader.style.display = 'none';
                }, 500);
            }
        }, 300);
    });
}

// ===== MOBILE OPTIMIZATIONS =====
function initMobileOptimizations() {
    // Detect mobile device
    const isMobile = window.matchMedia('(max-width: 575.98px)').matches;
    const isTouch = window.matchMedia('(hover: none) and (pointer: coarse)').matches;
    
    if (isMobile || isTouch) {
        document.body.classList.add('mobile-device');
        
        // Optimize viewport height for mobile browsers
        setViewportHeight();
        window.addEventListener('resize', setViewportHeight);
        
        // Prevent zoom on double tap
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function(e) {
            const now = Date.now();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        }, { passive: false });
        
        // Fix iOS scroll bounce
        document.body.addEventListener('touchmove', function(e) {
            if (e.target.closest('.modal, .glass-sidebar')) return;
        }, { passive: true });
    }
}

function setViewportHeight() {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}

// ===== SMOOTH SCROLLING =====
function initSmoothScrolling() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add page transition animation
    document.body.classList.add('page-transition');
}

// ===== FORM LOADING STATES =====
function initFormLoading() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Validate form before submitting
            if (!form.checkValidity()) {
                return;
            }
            
            // Add loading state
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('btn-loading');
                submitBtn.disabled = true;
                
                // Save original text
                if (!submitBtn.dataset.originalText) {
                    submitBtn.dataset.originalText = submitBtn.innerHTML;
                }
                
                submitBtn.innerHTML = 'Please wait...';
            }
            
            // Add form loading overlay
            form.classList.add('form-loading');
            
            // Disable all inputs
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => input.disabled = true);
        });
    });
}

// ===== TOUCH FEEDBACK =====
function initTouchFeedback() {
    const touchElements = document.querySelectorAll('.glass-btn, .nav-link, .card, .product-card');
    
    touchElements.forEach(el => {
        el.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
            this.style.opacity = '0.9';
        }, { passive: true });
        
        el.addEventListener('touchend', function() {
            this.style.transform = '';
            this.style.opacity = '';
        }, { passive: true });
    });
}

// ===== REDIRECT LOADING =====
function initRedirectLoading() {
    // Create redirect overlay if it doesn't exist
    if (!document.querySelector('.redirect-overlay')) {
        const overlay = document.createElement('div');
        overlay.className = 'redirect-overlay';
        overlay.innerHTML = `
            <div class="redirect-spinner"></div>
            <div class="redirect-text">Redirecting...</div>
        `;
        document.body.appendChild(overlay);
    }
    
    // Handle all internal link clicks
    document.querySelectorAll('a[href^="/"], a[href^="./"], a[href^="../"]').forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Skip if it's an anchor link or has special attributes
            if (href.startsWith('#') || 
                this.hasAttribute('download') || 
                this.hasAttribute('data-no-loader') ||
                this.target === '_blank') {
                return;
            }
            
            // Show redirect overlay
            const overlay = document.querySelector('.redirect-overlay');
            if (overlay) {
                overlay.classList.add('active');
            }
        });
    });
}

// ===== UTILITY FUNCTIONS =====

// Show loading spinner on any element
function showLoading(element, text = 'Loading...') {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }
    if (!element) return;
    
    element.classList.add('btn-loading');
    if (text) {
        element.dataset.originalText = element.innerHTML;
        element.innerHTML = text;
    }
}

// Hide loading spinner
function hideLoading(element) {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }
    if (!element) return;
    
    element.classList.remove('btn-loading');
    if (element.dataset.originalText) {
        element.innerHTML = element.dataset.originalText;
    }
}

// Show toast notification
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'x-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add styles
    toast.style.cssText = `
        position: fixed;
        bottom: 90px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(15, 23, 42, 0.95);
        color: white;
        padding: 12px 24px;
        border-radius: 50px;
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 14px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        animation: slideUp 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideDown 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// Add toast animations
const toastStyles = document.createElement('style');
toastStyles.textContent = `
    @keyframes slideUp {
        from { transform: translateX(-50%) translateY(100px); opacity: 0; }
        to { transform: translateX(-50%) translateY(0); opacity: 1; }
    }
    @keyframes slideDown {
        from { transform: translateX(-50%) translateY(0); opacity: 1; }
        to { transform: translateX(-50%) translateY(100px); opacity: 0; }
    }
`;
document.head.appendChild(toastStyles);

// Debounce function for performance
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

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Lazy load images
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// Initialize lazy loading
document.addEventListener('DOMContentLoaded', initLazyLoading);

// Handle back button for mobile
window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        // Page was loaded from cache (back button)
        const loader = document.querySelector('.page-loader');
        if (loader) {
            loader.style.display = 'none';
        }
    }
});

// Prevent double form submission
document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.dataset.submitting === 'true') {
        e.preventDefault();
        return;
    }
    form.dataset.submitting = 'true';
    
    // Reset after 5 seconds in case of error
    setTimeout(() => {
        form.dataset.submitting = 'false';
    }, 5000);
});

// Mobile menu toggle
function toggleMobileMenu() {
    const sidebar = document.querySelector('.glass-sidebar');
    if (sidebar) {
        sidebar.classList.toggle('mobile-open');
    }
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(e) {
    const sidebar = document.querySelector('.glass-sidebar');
    const toggle = document.querySelector('.mobile-menu-toggle');
    
    if (sidebar && sidebar.classList.contains('mobile-open')) {
        if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
            sidebar.classList.remove('mobile-open');
        }
    }
});

// Export functions for global access
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.showToast = showToast;
window.toggleMobileMenu = toggleMobileMenu;
