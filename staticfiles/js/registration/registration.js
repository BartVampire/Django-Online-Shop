document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('sign-form');
    const nextPageButton = document.getElementById('next-page');
    const errorMessage = document.querySelector('.error-message');
    const inputs = form.querySelectorAll('input');
    const navigationLinks = document.querySelectorAll('.navigation a');

    let currentInput = form.querySelector('.active');

    function showNextPage() {
        nextPageButton.style.opacity = '1';
    }

    function hideNextPage() {
        nextPageButton.style.opacity = '0';
    }

    function validateInput(input) {
        console.log('Validating input:', input.name, 'Value:', input.value);

        if (input.type === 'email' && !validateEmail(input.value)) {
            return false;
        }

        if (input.required && !input.value.trim()) {
            return false;
        }

        return true;
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.visibility = 'visible';
        errorMessage.style.opacity = '1';
    }

    function hideError() {
        errorMessage.textContent = '';
        errorMessage.style.visibility = 'hidden';
        errorMessage.style.opacity = '0';
    }

    function updateNextPageVisibility() {
        if (validateInput(currentInput)) {
            showNextPage();
            hideError();
        } else {
            hideNextPage();
        }
    }

    inputs.forEach(input => {
        input.addEventListener('input', function() {
            updateNextPageVisibility();
        });
    });

    navigationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('data-ref');
            const targetInput = document.getElementById(targetId);
            if (targetInput) {
                currentInput.classList.remove('active');
                targetInput.classList.add('active');
                currentInput = targetInput;
                targetInput.focus();
                updateNextPageVisibility();
            }
        });
    });

    nextPageButton.addEventListener('click', function() {
        console.log('Next button clicked. Current input:', currentInput.name);
        if (validateInput(currentInput)) {
            const nextLi = currentInput.closest('li').nextElementSibling;
            if (nextLi) {
                const nextInput = nextLi.querySelector('input');
                if (nextInput) {
                    currentInput.classList.remove('active');
                    nextInput.classList.add('active');
                    currentInput = nextInput;
                    nextInput.focus();
                    hideNextPage();
                }
            }
        } else {
            showError('Пожалуйста, заполните текущее поле');
        }
    });

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
});

