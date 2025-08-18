/**
 * Sistema de Convite de Casamento - JavaScript Principal
 * Iara & Samuel
 */

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeLoading();
    initializeNavigation();
    initializeScrollEffects();
    initializeAnimations();
    initializeFlashMessages();
    initializeForms();
    
    console.log('💕 Sistema de Convite Inicializado');
});

/**
 * Loading Screen
 */
function initializeLoading() {
    const loading = document.getElementById('loading');
    
    // Hide loading after page load
    window.addEventListener('load', function() {
        setTimeout(() => {
            if (loading) {
                loading.classList.add('hidden');
                setTimeout(() => {
                    loading.style.display = 'none';
                }, 500);
            }
        }, 1000);
    });
}

/**
 * Navigation
 */
function initializeNavigation() {
    const navbar = document.querySelector('.navbar');
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    const body = document.body;

    // Mobile menu toggle
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
            body.classList.toggle('nav-open');
            
            // Animate hamburger lines
            const spans = navToggle.querySelectorAll('span');
            if (navToggle.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });

        // Close menu when clicking on a link
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                body.classList.remove('nav-open');
                
                // Reset hamburger animation
                const spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });

        // Close menu when clicking on mobile overlay
        navMenu.addEventListener('click', function(e) {
            if (e.target === navMenu || e.target.classList.contains('nav-menu')) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                body.classList.remove('nav-open');
                
                // Reset hamburger animation
                const spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                body.classList.remove('nav-open');
                
                // Reset hamburger animation
                const spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });

        // Close menu on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && navMenu.classList.contains('active')) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                body.classList.remove('nav-open');
                
                // Reset hamburger animation
                const spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }

    // Navbar scroll effect with hide/show
    let lastScrollTop = 0;
    if (navbar) {
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
            
            // Hide/show navbar on scroll (only on mobile)
            if (window.innerWidth <= 768) {
                if (scrollTop > lastScrollTop && scrollTop > 200) {
                    navbar.style.transform = 'translateY(-100%)';
                } else {
                    navbar.style.transform = 'translateY(0)';
                }
            }
            
            lastScrollTop = scrollTop;
        });
    }

    // Active navigation highlighting
    function setActiveNavItem() {
        const currentPath = window.location.pathname;
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            
            const href = link.getAttribute('href');
            if ((currentPath === '/' && href === '/') || 
                (currentPath !== '/' && href !== '/' && currentPath.includes(href))) {
                link.classList.add('active');
            }
        });
    }
    
    setActiveNavItem();

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Scroll Effects
 */
function initializeScrollEffects() {
    // Parallax effect for hero section
    const hero = document.querySelector('.hero');
    if (hero) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.5;
            hero.style.transform = `translateY(${parallax}px)`;
        });
    }

    // Scroll indicator
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', function() {
            const welcomeSection = document.querySelector('.welcome-section');
            if (welcomeSection) {
                welcomeSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // Fade in on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const elementsToAnimate = document.querySelectorAll('.event-card, .gallery-item, .welcome-content');
    elementsToAnimate.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

/**
 * Animations
 */
function initializeAnimations() {
    // Countdown animation
    animateCountdown();
    
    // Gallery hover effects
    initializeGallery();
    
    // Button hover effects
    initializeButtonEffects();
}

function animateCountdown() {
    const countdownNumber = document.querySelector('.countdown-number');
    if (countdownNumber) {
        const finalNumber = parseInt(countdownNumber.textContent);
        let currentNumber = 0;
        const increment = finalNumber / 50; // Animation duration
        
        const timer = setInterval(() => {
            currentNumber += increment;
            if (currentNumber >= finalNumber) {
                currentNumber = finalNumber;
                clearInterval(timer);
            }
            countdownNumber.textContent = Math.floor(currentNumber);
        }, 20);
    }
}

function initializeGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const img = this.querySelector('img');
            if (img) {
                openLightbox(img.src, img.alt);
            }
        });
    });
}

function openLightbox(src, alt) {
    // Create lightbox
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.innerHTML = `
        <div class="lightbox-content">
            <img src="${src}" alt="${alt}">
            <button class="lightbox-close">&times;</button>
        </div>
    `;
    
    // Add styles
    lightbox.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    const content = lightbox.querySelector('.lightbox-content');
    content.style.cssText = `
        position: relative;
        max-width: 90%;
        max-height: 90%;
    `;
    
    const img = lightbox.querySelector('img');
    img.style.cssText = `
        width: 100%;
        height: 100%;
        object-fit: contain;
        border-radius: 10px;
    `;
    
    const closeBtn = lightbox.querySelector('.lightbox-close');
    closeBtn.style.cssText = `
        position: absolute;
        top: -40px;
        right: -40px;
        background: none;
        border: none;
        color: white;
        font-size: 2rem;
        cursor: pointer;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    
    document.body.appendChild(lightbox);
    
    // Animate in
    setTimeout(() => {
        lightbox.style.opacity = '1';
    }, 10);
    
    // Close handlers
    const closeLightbox = () => {
        lightbox.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(lightbox);
        }, 300);
    };
    
    closeBtn.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeLightbox();
        }
    });
}

function initializeButtonEffects() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
        
        btn.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(0) scale(0.98)';
        });
        
        btn.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(-2px) scale(1)';
        });
    });
}

/**
 * Flash Messages
 */
function initializeFlashMessages() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Auto close after 5 seconds
        setTimeout(() => {
            if (alert.parentElement) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (alert.parentElement) {
                        alert.remove();
                    }
                }, 300);
            }
        }, 5000);
        
        // Close button functionality
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                alert.style.opacity = '0';
                alert.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (alert.parentElement) {
                        alert.remove();
                    }
                }, 300);
            });
        }
    });
}

/**
 * Forms
 */
function initializeForms() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
            }
        });
    });

    // Input focus effects
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // Check if input has value on load
        if (input.value) {
            input.parentElement.classList.add('focused');
        }
    });
}

/**
 * Utility Functions
 */

// Format phone number
function formatPhone(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length >= 10) {
        value = value.replace(/(\d{2})(\d{4,5})(\d{4})/, '($1) $2-$3');
    } else if (value.length >= 6) {
        value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
    } else if (value.length >= 2) {
        value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    }
    input.value = value;
}

// Validate email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        ${message}
        <button class="alert-close">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    const container = document.querySelector('.flash-messages') || document.body;
    container.appendChild(notification);
    
    // Auto remove
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }
    }, 5000);
    
    // Close button
    const closeBtn = notification.querySelector('.alert-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        });
    }
}

// Debounce function
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

// Throttle function
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
    };
}

// Export functions for global use
window.ConviteApp = {
    showNotification,
    formatPhone,
    validateEmail,
    debounce,
    throttle
};

/**
 * Gifts Page Functionality
 */

// Initialize gifts page
function initializeGiftsPage() {
    if (!document.querySelector('.gifts-section')) return;
    
    initializeGiftFilters();
    initializeGiftCards();
    initializeGiftModal();
    initializeGiftAnimations();
    initializeGiftSearch();
    
    console.log('🎁 Página de Presentes Inicializada');
}

// Initialize gift search
function initializeGiftSearch() {
    const searchInput = document.getElementById('gift-search-input');
    const clearBtn = document.getElementById('clear-search');
    const giftCards = document.querySelectorAll('.gift-card');
    const emptyState = document.getElementById('empty-state');
    
    if (!searchInput) return;
    
    // Search functionality
    const performSearch = debounce(() => {
        const searchTerm = searchInput.value.toLowerCase().trim();
        
        if (searchTerm === '') {
            clearBtn.style.display = 'none';
            // Reset to current category filter
            const activeCategory = document.querySelector('.category-btn.active');
            if (activeCategory) {
                filterGifts(activeCategory.dataset.category, giftCards, emptyState);
            }
        } else {
            clearBtn.style.display = 'flex';
            filterGiftsBySearch(searchTerm, giftCards, emptyState);
        }
    }, 300);
    
    searchInput.addEventListener('input', performSearch);
    
    // Clear search
    clearBtn.addEventListener('click', () => {
        searchInput.value = '';
        clearBtn.style.display = 'none';
        // Reset to current category filter
        const activeCategory = document.querySelector('.category-btn.active');
        if (activeCategory) {
            filterGifts(activeCategory.dataset.category, giftCards, emptyState);
        }
        searchInput.focus();
    });
}

// Filter gifts by search term
function filterGiftsBySearch(searchTerm, giftCards, emptyState) {
    let visibleCount = 0;
    
    giftCards.forEach(card => {
        const giftName = card.querySelector('.gift-name').textContent.toLowerCase();
        const giftDescription = card.querySelector('.gift-description')?.textContent.toLowerCase() || '';
        
        const shouldShow = giftName.includes(searchTerm) || giftDescription.includes(searchTerm);
        
        if (shouldShow) {
            card.style.display = 'block';
            card.style.animation = 'fadeInUp 0.5s ease-out forwards';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    // Show/hide empty state
    if (emptyState) {
        if (visibleCount === 0) {
            emptyState.style.display = 'block';
            emptyState.querySelector('h3').textContent = 'Nenhum presente encontrado';
            emptyState.querySelector('p').textContent = `Não encontramos presentes com "${document.getElementById('gift-search-input').value}". Tente outro termo.`;
        } else {
            emptyState.style.display = 'none';
        }
    }
}

// Initialize gift card animations
function initializeGiftAnimations() {
    const giftCards = document.querySelectorAll('.gift-card');
    
    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100); // Stagger animation
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Set initial state and observe
    giftCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// Gift category filters
function initializeGiftFilters() {
    const categoryBtns = document.querySelectorAll('.category-btn');
    const giftCards = document.querySelectorAll('.gift-card');
    const emptyState = document.getElementById('empty-state');
    
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const category = this.dataset.category;
            
            // Update active button
            categoryBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Clear search if active
            const searchInput = document.getElementById('gift-search-input');
            if (searchInput && searchInput.value.trim() !== '') {
                searchInput.value = '';
                const clearBtn = document.getElementById('clear-search');
                if (clearBtn) clearBtn.style.display = 'none';
            }
            
            // Filter gifts
            filterGifts(category, giftCards, emptyState);
        });
    });
}

// Filter gifts by category
function filterGifts(category, giftCards, emptyState) {
    let visibleCount = 0;
    
    giftCards.forEach(card => {
        const cardCategory = card.dataset.category;
        const shouldShow = category === 'todos' || cardCategory === category;
        
        if (shouldShow) {
            card.style.display = 'block';
            card.style.animation = 'fadeInUp 0.5s ease-out forwards';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    // Show/hide empty state
    if (emptyState) {
        if (visibleCount === 0) {
            emptyState.style.display = 'block';
            emptyState.querySelector('h3').textContent = 'Nenhum presente encontrado';
            emptyState.querySelector('p').textContent = 'Não encontramos presentes nesta categoria. Tente outra categoria.';
        } else {
            emptyState.style.display = 'none';
        }
    }
}

// Gift cards interactions
function initializeGiftCards() {
    const giftCards = document.querySelectorAll('.gift-card');
    
    giftCards.forEach(card => {
        // Add click to view details
        card.addEventListener('click', function(e) {
            // Don't trigger if clicking on buttons
            if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A' || e.target.closest('button') || e.target.closest('a')) {
                return;
            }
            
            const giftId = this.dataset.id;
            showGiftModal(giftId);
        });
        
        // Add hover effects
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Gift modal functionality
function initializeGiftModal() {
    // Create modal if it doesn't exist
    if (!document.getElementById('gift-modal')) {
        createGiftModal();
    }
    
    const modal = document.getElementById('gift-modal');
    const closeBtn = modal.querySelector('.gift-modal-close');
    
    // Close modal events
    closeBtn.addEventListener('click', closeGiftModal);
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeGiftModal();
        }
    });
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeGiftModal();
        }
    });
}

// Create gift modal HTML
function createGiftModal() {
    const modalHTML = `
        <div class="gift-modal" id="gift-modal">
            <div class="gift-modal-content">
                <button class="gift-modal-close">
                    <i class="fas fa-times"></i>
                </button>
                <div class="gift-modal-body">
                    <!-- Content will be populated dynamically -->
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

// Show gift modal with details
function showGiftModal(giftId) {
    const modal = document.getElementById('gift-modal');
    const modalBody = modal.querySelector('.gift-modal-body');
    const giftCard = document.querySelector(`[data-id="${giftId}"]`);
    
    if (!giftCard) return;
    
    // Get gift data from card
    const giftData = extractGiftData(giftCard);
    
    // Populate modal content
    modalBody.innerHTML = createModalContent(giftData);
    
    // Show modal
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Initialize modal buttons
    initializeModalButtons(giftId);
}

// Extract gift data from card
function extractGiftData(giftCard) {
    const img = giftCard.querySelector('.gift-image img');
    const name = giftCard.querySelector('.gift-name').textContent;
    const description = giftCard.querySelector('.gift-description')?.textContent || '';
    const price = giftCard.querySelector('.gift-price span')?.textContent || '';
    const store = giftCard.querySelector('.gift-store span')?.textContent || '';
    const isAvailable = !giftCard.querySelector('.gift-chosen-badge');
    const storeLink = giftCard.querySelector('a[target="_blank"]')?.href || '';
    
    return {
        image: img?.src || '',
        name,
        description,
        price,
        store,
        isAvailable,
        storeLink
    };
}

// Create modal content HTML
function createModalContent(giftData) {
    return `
        <div class="gift-modal-image">
            ${giftData.image ? 
                `<img src="${giftData.image}" alt="${giftData.name}">` :
                `<div class="gift-placeholder"><i class="fas fa-gift"></i></div>`
            }
            ${!giftData.isAvailable ? 
                `<div class="gift-chosen-badge">
                    <i class="fas fa-check"></i>
                    <span>Escolhido</span>
                </div>` : ''
            }
        </div>
        
        <div class="gift-modal-info">
            <h2 class="gift-modal-title">${giftData.name}</h2>
            
            ${giftData.description ? 
                `<p class="gift-modal-description">${giftData.description}</p>` : ''
            }
            
            <div class="gift-modal-details">
                ${giftData.price ? 
                    `<div class="gift-detail">
                        <i class="fas fa-tag"></i>
                        <span>Preço sugerido: ${giftData.price}</span>
                    </div>` : ''
                }
                
                ${giftData.store ? 
                    `<div class="gift-detail">
                        <i class="fas fa-store"></i>
                        <span>Loja: ${giftData.store}</span>
                    </div>` : ''
                }
            </div>
            
            <div class="gift-modal-actions">
                ${giftData.isAvailable ? 
                    `<button class="btn btn-primary btn-large" onclick="chooseGiftFromModal()">
                        <i class="fas fa-heart"></i>
                        Escolher Este Presente
                    </button>` :
                    `<button class="btn btn-disabled btn-large" disabled>
                        <i class="fas fa-check"></i>
                        Já foi escolhido
                    </button>`
                }
                
                ${giftData.storeLink ? 
                    `<a href="${giftData.storeLink}" target="_blank" class="btn btn-outline btn-large">
                        <i class="fas fa-external-link-alt"></i>
                        Ver na Loja
                    </a>` : ''
                }
            </div>
        </div>
    `;
}

// Initialize modal buttons
function initializeModalButtons(giftId) {
    const modal = document.getElementById('gift-modal');
    const chooseBtn = modal.querySelector('button[onclick="chooseGiftFromModal()"]');
    
    if (chooseBtn) {
        chooseBtn.onclick = () => chooseGift(giftId);
    }
}

// Close gift modal
function closeGiftModal() {
    const modal = document.getElementById('gift-modal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

// Choose gift function (global)
window.chooseGift = function(giftId) {
    // Show confirmation dialog
    if (confirm('Você tem certeza que deseja escolher este presente?')) {
        // Create heart animation
        createHeartAnimation();
        
        // Here you would typically make an AJAX call to the server
        // For now, we'll just show a success message
        showNotification('Presente escolhido com sucesso! Obrigado pelo carinho ♥', 'success');
        
        // Update UI to show gift as chosen
        updateGiftAsChosen(giftId);
        
        // Close modal if open
        const modal = document.getElementById('gift-modal');
        if (modal.classList.contains('active')) {
            closeGiftModal();
        }
    }
};

// Create heart animation effect
function createHeartAnimation() {
    const heartsContainer = document.createElement('div');
    heartsContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
    `;
    
    // Create multiple hearts
    for (let i = 0; i < 12; i++) {
        const heart = document.createElement('div');
        heart.innerHTML = '♥';
        heart.style.cssText = `
            position: absolute;
            font-size: ${Math.random() * 20 + 20}px;
            color: #e91e63;
            left: ${Math.random() * 100}%;
            top: 100%;
            opacity: 0;
            animation: heartFloat 3s ease-out forwards;
            animation-delay: ${i * 0.1}s;
        `;
        heartsContainer.appendChild(heart);
    }
    
    document.body.appendChild(heartsContainer);
    
    // Remove after animation
    setTimeout(() => {
        if (heartsContainer.parentElement) {
            heartsContainer.remove();
        }
    }, 4000);
}

// Update gift card UI to show as chosen
function updateGiftAsChosen(giftId) {
    const giftCard = document.querySelector(`[data-id="${giftId}"]`);
    if (!giftCard) return;
    
    // Add chosen badge
    const giftImage = giftCard.querySelector('.gift-image');
    if (!giftImage.querySelector('.gift-chosen-badge')) {
        const badge = document.createElement('div');
        badge.className = 'gift-chosen-badge';
        badge.innerHTML = '<i class="fas fa-check"></i><span>Escolhido</span>';
        giftImage.appendChild(badge);
    }
    
    // Update button
    const actionBtn = giftCard.querySelector('.gift-actions button');
    if (actionBtn) {
        actionBtn.className = 'btn btn-disabled btn-block';
        actionBtn.disabled = true;
        actionBtn.innerHTML = '<i class="fas fa-check"></i> Já foi escolhido';
    }
    
    // Add animation
    giftCard.style.animation = 'pulse 1s ease-out';
}

// Initialize gifts page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeGiftsPage();
});

// Add CSS animations
const giftAnimations = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes heartFloat {
        0% {
            opacity: 0;
            transform: translateY(0) rotate(0deg);
        }
        10% {
            opacity: 1;
        }
        100% {
            opacity: 0;
            transform: translateY(-100vh) rotate(360deg);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -200px 0;
        }
        100% {
            background-position: calc(200px + 100%) 0;
        }
    }
    
    .gift-card.loading .gift-image::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.4),
            transparent
        );
        background-size: 200px 100%;
        animation: shimmer 1.5s infinite;
    }
`;

// Inject animations
if (!document.getElementById('gift-animations')) {
    const style = document.createElement('style');
    style.id = 'gift-animations';
    style.textContent = giftAnimations;
    document.head.appendChild(style);
}
