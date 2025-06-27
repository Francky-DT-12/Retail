// Product Details Page JavaScript

// Change main image when thumbnail is clicked
function changeMainImage(src) {
    const mainImage = document.getElementById('mainProductImage');
    const thumbnails = document.querySelectorAll('.thumbnail');
    
    if (mainImage) {
        mainImage.src = src;
    }
    
    // Update active thumbnail
    thumbnails.forEach(thumb => {
        thumb.classList.remove('active');
        if (thumb.src === src) {
            thumb.classList.add('active');
        }
    });
}

// Quantity controls with data attributes
function increaseQuantity(maxQuantity) {
    const quantityInput = document.getElementById('quantity');
    if (quantityInput) {
        let currentValue = parseInt(quantityInput.value) || 1;
        if (currentValue < maxQuantity) {
            quantityInput.value = currentValue + 1;
        }
    }
}

function decreaseQuantity() {
    const quantityInput = document.getElementById('quantity');
    if (quantityInput) {
        let currentValue = parseInt(quantityInput.value) || 1;
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    }
}

// Enhanced DOMContentLoaded with new features
document.addEventListener('DOMContentLoaded', function() {
    const colorOptions = document.querySelectorAll('.color-option');
    const sizeOptions = document.querySelectorAll('.size-option');
    const quantityBtns = document.querySelectorAll('.quantity-btn');
    const filterBtns = document.querySelectorAll('.filter-btn');
    
    // Quantity controls using data attributes
    quantityBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-action');
            const quantityInput = document.getElementById('quantity');
            
            if (action === 'increase') {
                const maxQuantity = parseInt(this.getAttribute('data-max')) || 999;
                increaseQuantity(maxQuantity);
            } else if (action === 'decrease') {
                decreaseQuantity();
            }
        });
    });
    
    // Color selection handlers
    colorOptions.forEach(option => {
        option.addEventListener('click', function() {
            colorOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
            
            // You can add logic here to change product images based on color
            const selectedColor = this.getAttribute('data-color');
            console.log('Selected color:', selectedColor);
        });
    });
    
    // Size selection handlers
    sizeOptions.forEach(option => {
        option.addEventListener('click', function() {
            sizeOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
            
            const selectedSize = this.getAttribute('data-size');
            console.log('Selected size:', selectedSize);
        });
    });
    
    // Review filters
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            filterBtns.forEach(f => f.classList.remove('active'));
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            console.log('Filter applied:', filter);
            // Add logic to filter reviews based on selection
        });
    });
    
    // Product action buttons
    const wishlistBtn = document.querySelector('.wishlist-btn');
    const compareBtn = document.querySelector('.compare-btn');
    const shareBtn = document.querySelector('.share-btn');
    
    // Enhanced product action handlers
    const actionBtns = document.querySelectorAll('.action-btn');
    actionBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
    
    // Wishlist functionality
    if (wishlistBtn) {
        wishlistBtn.addEventListener('click', function() {
            this.classList.toggle('active');
            const icon = this.querySelector('i');
            if (this.classList.contains('active')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                showToast('Added to wishlist!', 'success');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                showToast('Removed from wishlist', 'info');
            }
        });
    }
    
    // Share functionality
    if (shareBtn) {
        shareBtn.addEventListener('click', function() {
            if (navigator.share) {
                navigator.share({
                    title: document.querySelector('.product-title').textContent,
                    text: 'Check out this amazing product!',
                    url: window.location.href
                });
            } else {
                // Fallback: copy to clipboard
                navigator.clipboard.writeText(window.location.href).then(() => {
                    showToast('Product URL copied to clipboard!', 'success');
                }).catch(() => {
                    showToast('Unable to copy URL', 'error');
                });
            }
        });
    }
    
    // Image zoom functionality
    const mainImageContainer = document.querySelector('.main-image');
    if (mainImageContainer) {
        mainImageContainer.addEventListener('click', function() {
            const img = this.querySelector('img');
            if (img) {
                // Create modal for image zoom
                const modal = document.createElement('div');
                modal.className = 'image-zoom-modal';
                modal.innerHTML = `
                    <div class="zoom-modal-content">
                        <span class="close-zoom">&times;</span>
                        <img src="${img.src}" alt="${img.alt}">
                    </div>
                `;
                document.body.appendChild(modal);
                
                // Close modal handlers
                const closeBtn = modal.querySelector('.close-zoom');
                closeBtn.addEventListener('click', () => modal.remove());
                modal.addEventListener('click', (e) => {
                    if (e.target === modal) modal.remove();
                });
            }
        });
    }
    
    // Enhanced image gallery with zoom indicator
    const zoomIcon = document.querySelector('.zoom-icon');
    if (zoomIcon) {
        zoomIcon.addEventListener('click', function(e) {
            e.stopPropagation();
            // Implement full-screen image gallery
            const imageUrl = document.getElementById('mainProductImage').src;
            openImageModal(imageUrl);
        });
    }
    
    // Load more reviews functionality
    const loadMoreBtn = document.querySelector('.load-more-btn');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function() {
            // Add logic to load more reviews
            console.log('Loading more reviews...');
            // You can make an AJAX request here to fetch more reviews
        });
    }
    
    // Add to cart form validation
    const addToCartForm = document.querySelector('.add-to-cart-form');
    if (addToCartForm) {
        addToCartForm.addEventListener('submit', function(e) {
            const selectedColor = document.querySelector('.color-option.selected');
            const selectedSize = document.querySelector('.size-option.selected');
            
            if (!selectedColor) {
                e.preventDefault();
                alert('Please select a color');
                return;
            }
            
            if (!selectedSize) {
                e.preventDefault();
                alert('Please select a size');
                return;
            }
            
            // If all validations pass, the form will submit normally
            console.log('Adding to cart with:', {
                color: selectedColor.getAttribute('data-color'),
                size: selectedSize.getAttribute('data-size'),
                quantity: document.getElementById('quantity').value
            });
        });
    }
    
    // Product image zoom functionality (optional enhancement)
    const mainImage = document.getElementById('mainProductImage');
    if (mainImage) {
        mainImage.addEventListener('click', function() {
            // You can add zoom functionality here
            console.log('Image clicked - could implement zoom');
        });
    }
    
    // Smooth scroll for related products
    const relatedProductLinks = document.querySelectorAll('.related-products-section .product-link');
    relatedProductLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Add loading state or smooth transition
            console.log('Navigating to product:', this.href);
        });
    });
    
    // Add some interactive feedback
    const quantityButtons = document.querySelectorAll('.quantity-btn');
    quantityButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
        });
    });
    
    // Add hover effects for product cards
    const productCards = document.querySelectorAll('.product-card-modern');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
    
    // Image zoom modal functionality
    function openImageModal(imageSrc) {
        // Create modal
        const modal = document.createElement('div');
        modal.className = 'image-modal';
        modal.innerHTML = `
            <div class="image-modal-overlay">
                <div class="image-modal-content">
                    <button class="modal-close">&times;</button>
                    <img src="${imageSrc}" alt="Product Image">
                    <div class="modal-nav">
                        <button class="modal-prev">‹</button>
                        <button class="modal-next">›</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        document.body.style.overflow = 'hidden';
        
        // Modal styles
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        
        // Close modal functionality
        const closeModal = () => {
            document.body.removeChild(modal);
            document.body.style.overflow = 'auto';
        };
        
        modal.querySelector('.modal-close').addEventListener('click', closeModal);
        modal.querySelector('.image-modal-overlay').addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });
        
        // ESC key to close
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') closeModal();
        });
    }
    
    // Enhanced form submission with loading state
    const addToCartForm = document.querySelector('.add-to-cart-form');
    if (addToCartForm) {
        addToCartForm.addEventListener('submit', function() {
            const submitBtn = this.querySelector('.add-to-cart-btn');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
            submitBtn.disabled = true;
            
            // Reset after 2 seconds (for demo purposes)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                showToast('Product added to cart!', 'success');
            }, 2000);
        });
    }
});

// Toast notification for add to cart (optional)
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas fa-${type === 'success' ? 'check' : 'exclamation'}-circle"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add toast styles
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : '#dc3545'};
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 100);
    
    // Hide toast after 3 seconds
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}
