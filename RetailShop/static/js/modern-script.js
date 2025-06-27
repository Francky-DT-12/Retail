// Modern JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Close header notification
    const closeBtn = document.querySelector('.close-btn');
    const headerTop = document.querySelector('.header-top');
    
    if (closeBtn && headerTop) {
        closeBtn.addEventListener('click', function() {
            headerTop.style.display = 'none';
        });
    }

    // Search functionality
    const searchInput = document.querySelector('.search-box input');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.parentElement.style.boxShadow = '0 0 0 2px rgba(0,0,0,0.1)';
        });
        
        searchInput.addEventListener('blur', function() {
            this.parentElement.style.boxShadow = 'none';
        });
    }

    // Product card hover effects
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 10px 30px rgba(0,0,0,0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.boxShadow = 'none';
        });
    });

    // Smooth scroll for navigation links
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Only prevent default for hash links
            if (this.getAttribute('href').startsWith('#')) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Newsletter form submission
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            
            if (email) {
                // Here you would typically send the email to your server
                alert('Thank you for subscribing to our newsletter!');
                this.querySelector('input[type="email"]').value = '';
            } else {
                alert('Please enter a valid email address.');
            }
        });
    }

    // Add to cart functionality (placeholder)
    const shopNowBtn = document.querySelector('.shop-now-btn');
    if (shopNowBtn) {
        shopNowBtn.addEventListener('click', function() {
            // Scroll to products section
            const productsSection = document.querySelector('.new-arrivals');
            if (productsSection) {
                productsSection.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    }

    // Dropdown menu functionality - Updated to work with Bootstrap
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(toggle => {
        const dropdownMenu = toggle.nextElementSibling;
        
        if (dropdownMenu && dropdownMenu.classList.contains('dropdown-menu')) {
            // For desktop - add hover functionality
            const dropdown = toggle.closest('.dropdown');
            
            if (dropdown && window.innerWidth > 767) {
                dropdown.addEventListener('mouseenter', function() {
                    if (!dropdownMenu.classList.contains('show')) {
                        // Use Bootstrap's dropdown API
                        $(toggle).dropdown('show');
                    }
                });
                
                dropdown.addEventListener('mouseleave', function() {
                    if (dropdownMenu.classList.contains('show')) {
                        // Use Bootstrap's dropdown API
                        $(toggle).dropdown('hide');
                    }
                });
            }
        }
    });

    // View all buttons
    const viewAllBtns = document.querySelectorAll('.view-all-btn');
    viewAllBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Get the parent section to determine which "View All" was clicked
            const parentSection = this.closest('.new-arrivals, .top-selling');
            if (parentSection) {
                if (parentSection.classList.contains('new-arrivals')) {
                    window.location.href = '/arrivals';
                } else if (parentSection.classList.contains('top-selling')) {
                    window.location.href = '/sales';
                }
            } else {
                // Default to all products
                window.location.href = '/all-products';
            }
        });
    });

    // Style cards click functionality
    const styleCards = document.querySelectorAll('.style-card');
    styleCards.forEach(card => {
        card.addEventListener('click', function() {
            const style = this.querySelector('h3').textContent.toLowerCase();
            console.log(`Browse ${style} style clicked`);
            // Here you would typically redirect to a filtered products page
        });
    });

    // Simple animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Apply fade-in animation to sections
    const sections = document.querySelectorAll('.new-arrivals, .top-selling, .browse-style, .testimonials');
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });

    // Mobile menu toggle (if needed)
    const navMenu = document.querySelector('.nav-menu');
    const hamburger = document.querySelector('.hamburger');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }

    // Cart icon animation
    const cartIcon = document.querySelector('.fa-shopping-cart');
    if (cartIcon) {
        cartIcon.addEventListener('click', function() {
            this.style.transform = 'scale(1.2)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    }

    // Product image lazy loading
    const productImages = document.querySelectorAll('.product-image img');
    const imageObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.style.opacity = '1';
                imageObserver.unobserve(img);
            }
        });
    });

    productImages.forEach(img => {
        img.style.opacity = '0.5';
        img.style.transition = 'opacity 0.3s ease';
        imageObserver.observe(img);
    });

    // Star rating animation
    const starContainers = document.querySelectorAll('.stars');
    starContainers.forEach(container => {
        const stars = container.querySelectorAll('.fa-star, .fa-star-half-alt');
        stars.forEach((star, index) => {
            star.style.animationDelay = `${index * 0.1}s`;
            star.style.animation = 'starGlow 2s ease-in-out infinite';
        });
    });
});

// Add CSS for star animation
const style = document.createElement('style');
style.textContent = `
    @keyframes starGlow {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .fa-star, .fa-star-half-alt {
        transition: transform 0.2s ease;
    }
    
    .product-card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .style-card {
        transition: transform 0.3s ease;
    }
    
    .nav-menu a:hover {
        color: #666;
        transition: color 0.3s ease;
    }
`;
document.head.appendChild(style);
