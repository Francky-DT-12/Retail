/**
 * Mobile Responsive JavaScript
 * Gestion des interactions mobiles
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ===========================================
    // MOBILE HAMBURGER MENU
    // ===========================================
    
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenuContainer = document.querySelector('.nav-menu-container');
    const body = document.body;
    
    if (mobileMenuToggle && navMenuContainer) {
        // Toggle mobile menu
        mobileMenuToggle.addEventListener('click', function() {
            const isActive = navMenuContainer.classList.contains('active');
            
            if (isActive) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInsideNav = navMenuContainer.contains(event.target);
            const isClickOnToggle = mobileMenuToggle.contains(event.target);
            
            if (!isClickInsideNav && !isClickOnToggle && navMenuContainer.classList.contains('active')) {
                closeMobileMenu();
            }
        });
        
        // Close menu when pressing escape
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && navMenuContainer.classList.contains('active')) {
                closeMobileMenu();
            }
        });
        
        // Close menu when clicking on a nav link
        const navLinks = navMenuContainer.querySelectorAll('.nav-menu a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                closeMobileMenu();
            });
        });
    }
    
    function openMobileMenu() {
        navMenuContainer.classList.add('active');
        mobileMenuToggle.classList.add('active');
        body.style.overflow = 'hidden'; // Prevent scrolling when menu is open
        mobileMenuToggle.setAttribute('aria-expanded', 'true');
    }
    
    function closeMobileMenu() {
        navMenuContainer.classList.remove('active');
        mobileMenuToggle.classList.remove('active');
        body.style.overflow = '';
        mobileMenuToggle.setAttribute('aria-expanded', 'false');
    }
    
    // ===========================================
    // MOBILE RESPONSIVE UTILITIES
    // ===========================================
    
    // Detect mobile device
    function isMobile() {
        return window.innerWidth <= 768;
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (!isMobile() && navMenuContainer && navMenuContainer.classList.contains('active')) {
            closeMobileMenu();
        }
        
        // Update viewport height for mobile browsers
        updateViewportHeight();
    });
    
    // Update viewport height for mobile browsers (addresses URL bar issue)
    function updateViewportHeight() {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
    
    updateViewportHeight();
    
    // ===========================================
    // MOBILE TOUCH IMPROVEMENTS
    // ===========================================
    
    // Add touch feedback for buttons
    const touchElements = document.querySelectorAll('.btn, .icon-link, .card, .product-card');
    
    touchElements.forEach(element => {
        element.addEventListener('touchstart', function() {
            this.classList.add('touch-active');
        });
        
        element.addEventListener('touchend', function() {
            setTimeout(() => {
                this.classList.remove('touch-active');
            }, 150);
        });
        
        element.addEventListener('touchcancel', function() {
            this.classList.remove('touch-active');
        });
    });
    
    // ===========================================
    // MOBILE FORM IMPROVEMENTS
    // ===========================================
    
    // Improve mobile form experience
    const formInputs = document.querySelectorAll('input, textarea, select');
    
    formInputs.forEach(input => {
        // Add focus states for better mobile interaction
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('input-focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('input-focused');
        });
        
        // Prevent zoom on iOS for inputs with font-size < 16px
        if (isMobile() && input.type !== 'range') {
            const currentFontSize = window.getComputedStyle(input).fontSize;
            const fontSize = parseFloat(currentFontSize);
            
            if (fontSize < 16) {
                input.style.fontSize = '16px';
            }
        }
    });
    
    // ===========================================
    // MOBILE TABLE IMPROVEMENTS
    // ===========================================
    
    // Convert tables to card layout on mobile
    function makeTablesResponsive() {
        const tables = document.querySelectorAll('.table-responsive table');
        
        tables.forEach(table => {
            if (isMobile()) {
                makeTableCardStyle(table);
            }
        });
    }
    
    function makeTableCardStyle(table) {
        const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            cells.forEach((cell, index) => {
                if (headers[index]) {
                    cell.setAttribute('data-label', headers[index]);
                }
            });
        });
        
        table.classList.add('table-cards');
    }
    
    // Initialize responsive tables
    makeTablesResponsive();
    
    // ===========================================
    // MOBILE SCROLL IMPROVEMENTS
    // ===========================================
    
    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            const target = document.querySelector(href);
            
            if (target) {
                e.preventDefault();
                
                const headerHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // ===========================================
    // MOBILE IMAGE LAZY LOADING
    // ===========================================
    
    // Simple lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => imageObserver.observe(img));
    }
    
    // ===========================================
    // MOBILE MODAL IMPROVEMENTS
    // ===========================================
    
    // Improve modal behavior on mobile
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            if (isMobile()) {
                body.style.position = 'fixed';
                body.style.top = `-${window.scrollY}px`;
                body.style.width = '100%';
            }
        });
        
        modal.addEventListener('hidden.bs.modal', function() {
            if (isMobile()) {
                const scrollY = body.style.top;
                body.style.position = '';
                body.style.top = '';
                body.style.width = '';
                window.scrollTo(0, parseInt(scrollY || '0') * -1);
            }
        });
    });
    
    // ===========================================
    // MOBILE SWIPE GESTURES
    // ===========================================
    
    // Simple swipe detection for carousels and product galleries
    let touchStartX = 0;
    let touchEndX = 0;
    
    function handleSwipe(element, leftCallback, rightCallback) {
        element.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        });
        
        element.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipeGesture(leftCallback, rightCallback);
        });
    }
    
    function handleSwipeGesture(leftCallback, rightCallback) {
        const swipeThreshold = 50;
        const swipeDistance = touchEndX - touchStartX;
        
        if (Math.abs(swipeDistance) > swipeThreshold) {
            if (swipeDistance > 0 && rightCallback) {
                rightCallback();
            } else if (swipeDistance < 0 && leftCallback) {
                leftCallback();
            }
        }
    }
    
    // Apply swipe gestures to carousels
    const carousels = document.querySelectorAll('.carousel, .product-gallery');
    carousels.forEach(carousel => {
        const prevBtn = carousel.querySelector('.carousel-control-prev, .prev-btn');
        const nextBtn = carousel.querySelector('.carousel-control-next, .next-btn');
        
        if (prevBtn && nextBtn) {
            handleSwipe(
                carousel,
                () => nextBtn.click(), // Swipe left -> next
                () => prevBtn.click()  // Swipe right -> prev
            );
        }
    });
    
    // ===========================================
    // MOBILE PERFORMANCE OPTIMIZATIONS
    // ===========================================
    
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
    
    // Use throttled resize handler
    const throttledResize = throttle(() => {
        updateViewportHeight();
        makeTablesResponsive();
    }, 250);
    
    window.addEventListener('resize', throttledResize);
    
    // ===========================================
    // MOBILE ACCESSIBILITY IMPROVEMENTS
    // ===========================================
    
    // Improve focus management for mobile
    const focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
    
    // Add visible focus indicators for keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-navigation');
    });
    
    // ===========================================
    // MOBILE INITIALIZATION
    // ===========================================
    
    console.log('Mobile responsive JavaScript initialized');
    
    // Add mobile class to body for CSS targeting
    if (isMobile()) {
        document.body.classList.add('mobile-device');
    }
    
    // Update mobile class on resize
    window.addEventListener('resize', debounce(() => {
        if (isMobile()) {
            document.body.classList.add('mobile-device');
        } else {
            document.body.classList.remove('mobile-device');
        }
    }, 250));
    
});
