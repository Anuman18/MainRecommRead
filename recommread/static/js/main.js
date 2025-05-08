// Main JS file for RecommRead application

document.addEventListener('DOMContentLoaded', function() {
    // Handle flash message dismissal
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        const closeBtn = message.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                }, 300);
            });
            
            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                }, 300);
            }, 5000);
        }
    });

    // Toggle mobile menu
    const menuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (menuButton && mobileMenu) {
        menuButton.addEventListener('click', () => {
            const expanded = menuButton.getAttribute('aria-expanded') === 'true';
            menuButton.setAttribute('aria-expanded', !expanded);
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Handle vote buttons
    const voteButtons = document.querySelectorAll('.vote-btn');
    voteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // The actual vote functionality is handled server-side
            // This is just for visual feedback
            button.classList.add('voted');
            
            // Add a brief animation
            button.style.transform = 'scale(1.2)';
            setTimeout(() => {
                button.style.transform = 'scale(1)';
            }, 200);
        });
    });

    // Add character counter for post content
    const contentTextarea = document.querySelector('textarea[name="content"]');
    const characterCounter = document.getElementById('character-counter');
    
    if (contentTextarea && characterCounter) {
        contentTextarea.addEventListener('input', function() {
            const remaining = 2000 - this.value.length;
            characterCounter.textContent = `${this.value.length} characters (${remaining} remaining)`;
            
            if (remaining < 0) {
                characterCounter.classList.add('text-red-500');
            } else {
                characterCounter.classList.remove('text-red-500');
            }
        });
        
        // Trigger on load to show initial count
        contentTextarea.dispatchEvent(new Event('input'));
    }

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const target = document.querySelector(targetId);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});
