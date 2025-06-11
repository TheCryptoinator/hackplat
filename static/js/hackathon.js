// Initialize Bootstrap tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Handle announcement modal
const announcementModal = document.getElementById('announcementModal');
if (announcementModal) {
    announcementModal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const modalTitle = announcementModal.querySelector('.modal-title');
        modalTitle.textContent = 'New Announcement';
    });
}

// Handle team join confirmation
const joinTeamForms = document.querySelectorAll('form[action*="join_team"]');
joinTeamForms.forEach(form => {
    form.addEventListener('submit', function(event) {
        if (!confirm('Are you sure you want to join this team?')) {
            event.preventDefault();
        }
    });
});

// Handle registration confirmation
const registerForm = document.querySelector('form[action*="register_for_hackathon"]');
if (registerForm) {
    registerForm.addEventListener('submit', function(event) {
        const button = this.querySelector('button[type="submit"]');
        if (button.textContent.includes('Waitlist')) {
            if (!confirm('This hackathon has reached its capacity. You will be added to the waitlist. Continue?')) {
                event.preventDefault();
            }
        }
    });
}

// Auto-update capacity progress bar
function updateCapacityBar() {
    const capacityBar = document.querySelector('.progress-bar');
    if (capacityBar) {
        const current = parseInt(capacityBar.getAttribute('aria-valuenow'));
        const max = parseInt(capacityBar.getAttribute('aria-valuemax'));
        const percentage = (current / max) * 100;
        capacityBar.style.width = percentage + '%';
        
        // Update color based on capacity
        if (percentage >= 90) {
            capacityBar.classList.remove('bg-success', 'bg-warning');
            capacityBar.classList.add('bg-danger');
        } else if (percentage >= 75) {
            capacityBar.classList.remove('bg-success', 'bg-danger');
            capacityBar.classList.add('bg-warning');
        } else {
            capacityBar.classList.remove('bg-warning', 'bg-danger');
            capacityBar.classList.add('bg-success');
        }
    }
}

// Call updateCapacityBar on page load
document.addEventListener('DOMContentLoaded', updateCapacityBar);

// Handle track badges hover effect
const trackBadges = document.querySelectorAll('.badge.bg-primary');
trackBadges.forEach(badge => {
    badge.addEventListener('mouseover', function() {
        this.style.cursor = 'pointer';
    });
    badge.addEventListener('click', function() {
        const track = this.textContent.trim();
        // You can implement track filtering here
        console.log('Selected track:', track);
    });
});

// Handle sponsor logo loading errors
const sponsorLogos = document.querySelectorAll('.sponsor-logo');
sponsorLogos.forEach(img => {
    img.addEventListener('error', function() {
        this.src = '/static/images/default-sponsor.png';
        this.alt = 'Sponsor logo not available';
    });
}); 