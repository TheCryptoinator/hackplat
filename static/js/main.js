// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add fade-in animation to cards
    document.querySelectorAll('.card').forEach(function(card) {
        card.classList.add('fade-in');
    });

    // Handle form submissions with AJAX
    document.querySelectorAll('form[data-ajax="true"]').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const submitButton = form.querySelector('[type="submit"]');
            const originalText = submitButton.innerHTML;
            
            // Disable submit button and show loading state
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
            
            fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Show success message
                if (data.success) {
                    showAlert('success', data.message);
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                } else {
                    showAlert('danger', data.message || 'An error occurred');
                }
            })
            .catch(error => {
                showAlert('danger', 'An error occurred while processing your request');
                console.error('Error:', error);
            })
            .finally(() => {
                // Reset submit button
                submitButton.disabled = false;
                submitButton.innerHTML = originalText;
            });
        });
    });

    // Function to show alerts
    function showAlert(type, message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    // Handle dynamic form fields
    document.querySelectorAll('[data-add-field]').forEach(function(button) {
        button.addEventListener('click', function() {
            const template = document.querySelector(this.dataset.template);
            const container = document.querySelector(this.dataset.target);
            const clone = template.content.cloneNode(true);
            container.appendChild(clone);
        });
    });

    // Handle file upload previews
    document.querySelectorAll('input[type="file"]').forEach(function(input) {
        input.addEventListener('change', function() {
            const preview = document.querySelector(this.dataset.preview);
            if (preview && this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    // Handle dynamic search
    let searchTimeout;
    document.querySelectorAll('[data-search]').forEach(function(input) {
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const searchTerm = this.value;
                const target = document.querySelector(this.dataset.target);
                
                if (searchTerm.length >= 2) {
                    fetch(`/api/search?q=${encodeURIComponent(searchTerm)}`)
                        .then(response => response.json())
                        .then(data => {
                            // Update the target element with search results
                            if (target) {
                                target.innerHTML = data.results.map(result => `
                                    <div class="search-result">
                                        <h5>${result.title}</h5>
                                        <p>${result.description}</p>
                                    </div>
                                `).join('');
                            }
                        })
                        .catch(error => console.error('Search error:', error));
                }
            }, 300);
        });
    });

    // Handle infinite scroll
    let page = 1;
    let loading = false;
    const loadMoreButton = document.querySelector('[data-load-more]');
    
    if (loadMoreButton) {
        window.addEventListener('scroll', function() {
            if (loading) return;
            
            const rect = loadMoreButton.getBoundingClientRect();
            if (rect.top <= window.innerHeight) {
                loading = true;
                page++;
                
                fetch(`/api/load-more?page=${page}`)
                    .then(response => response.json())
                    .then(data => {
                        const container = document.querySelector(loadMoreButton.dataset.target);
                        container.insertAdjacentHTML('beforeend', data.html);
                        loading = false;
                        
                        if (!data.hasMore) {
                            loadMoreButton.style.display = 'none';
                        }
                    })
                    .catch(error => {
                        console.error('Load more error:', error);
                        loading = false;
                    });
            }
        });
    }
}); 