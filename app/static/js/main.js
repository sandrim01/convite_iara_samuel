// Modern Wedding Invitation JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Navbar scroll effect
    const navbar = document.getElementById('mainNavbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // Active nav link highlighting
    const sections = document.querySelectorAll('section[id]');
    const navItems = document.querySelectorAll('.navbar-nav .nav-link');
    
    function highlightNavLink() {
        let currentSection = '';
        
        sections.forEach(section => {
            const sectionTop = section.getBoundingClientRect().top;
            const sectionHeight = section.offsetHeight;
            
            if (sectionTop <= 100 && sectionTop + sectionHeight > 100) {
                currentSection = section.getAttribute('id');
            }
        });
        
        navItems.forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('href') === `#${currentSection}`) {
                item.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', highlightNavLink);
    
    // Parallax effect for hero section
    const hero = document.querySelector('.hero-wedding');
    if (hero) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.5;
            hero.style.transform = `translateY(${parallax}px)`;
        });
    }
    
    // Countdown timer animation
    function animateCountdown() {
        const countdownNumber = document.getElementById('days');
        if (countdownNumber) {
            countdownNumber.style.transform = 'scale(1.1)';
            setTimeout(() => {
                countdownNumber.style.transform = 'scale(1)';
            }, 200);
        }
    }
    
    // Animate countdown every hour
    setInterval(animateCountdown, 3600000);
    
    // Floating hearts animation
    function createFloatingHeart() {
        const heart = document.createElement('div');
        heart.innerHTML = '♥';
        heart.className = 'floating-heart';
        heart.style.cssText = `
            position: fixed;
            color: rgba(212, 165, 116, 0.3);
            font-size: ${Math.random() * 20 + 10}px;
            left: ${Math.random() * 100}vw;
            animation: floatUp 4s linear forwards;
            pointer-events: none;
            z-index: 1;
        `;
        
        document.body.appendChild(heart);
        
        setTimeout(() => {
            heart.remove();
        }, 4000);
    }
    
    // Add floating hearts periodically
    setInterval(createFloatingHeart, 3000);
    
    // Add CSS for floating hearts animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes floatUp {
            0% {
                transform: translateY(100vh) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100px) rotate(360deg);
                opacity: 0;
            }
        }
        
        .floating-heart {
            transition: all 0.3s ease;
        }
    `;
    document.head.appendChild(style);
    
    // Image lazy loading for better performance
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Form validation and enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Por favor, preencha todos os campos obrigatórios.');
            }
        });
    });
    
    // Mobile menu enhancement
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });
    }
    
    // Preloader
    const preloader = document.getElementById('preloader');
    if (preloader) {
        window.addEventListener('load', () => {
            preloader.style.opacity = '0';
            setTimeout(() => {
                preloader.style.display = 'none';
            }, 500);
        });
    }
    
    console.log('🌹 Wedding invitation loaded successfully! 💕');
});

// Utility functions
function formatDate(date) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        locale: 'pt-BR' 
    };
    return new Date(date).toLocaleDateString('pt-BR', options);
}

function shareInvitation() {
    if (navigator.share) {
        navigator.share({
            title: 'Convite de Casamento - Iara & Samuel',
            text: 'Você está convidado para o nosso casamento!',
            url: window.location.href
        });
    } else {
        // Fallback for browsers that don't support Web Share API
        const url = window.location.href;
        navigator.clipboard.writeText(url).then(() => {
            alert('Link copiado para a área de transferência!');
        });
    }
}

// Export functions for global use
window.shareInvitation = shareInvitation;
