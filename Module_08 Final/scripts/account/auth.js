// Notification Module
const NotificationModule = {
    notificationTypes: {
        success: {
            icon: '<i class="bi bi-check-circle-fill me-2"></i>',
            bgColor: 'bg-success'
        },
        error: {
            icon: '<i class="bi bi-x-circle-fill me-2"></i>',
            bgColor: 'bg-danger'
        },
        warning: {
            icon: '<i class="bi bi-exclamation-triangle-fill me-2"></i>',
            bgColor: 'bg-warning'
        },
        info: {
            icon: '<i class="bi bi-info-circle-fill me-2"></i>',
            bgColor: 'bg-info'
        }
    },

    showNotification(message, type = 'info', duration = 3000) {
        const { icon, bgColor } = this.notificationTypes[type] || this.notificationTypes.info;
        const notificationContainer = document.getElementById('notification-container');
        
        if (!notificationContainer) return;

        const notification = document.createElement('div');
        notification.className = `${bgColor} text-white rounded-3 shadow-lg p-3 mb-2 d-flex align-items-center notification-popup`;
        notification.style.cssText = `
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease-in-out;
            max-width: 300px;
            margin-left: auto;
        `;

        notification.innerHTML = `
            ${icon}
            <span class="mx-2">${message}</span>
            <button type="button" class="btn-close btn-close-white ms-2" 
                    style="font-size: 0.8rem;" aria-label="Close"></button>
        `;

        notificationContainer.appendChild(notification);

        requestAnimationFrame(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        });

        const closeButton = notification.querySelector('.btn-close');
        closeButton.addEventListener('click', () => this.closeNotification(notification));

        if (duration > 0) {
            setTimeout(() => this.closeNotification(notification), duration);
        }
    },

    closeNotification(notification) {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => notification.remove(), 300);
    }
};

// UI Module
const UIModule = {
    showLoggedIn(username) {
        document.getElementById('auth-forms-container').classList.add('d-none');
        document.getElementById('user-info').classList.remove('d-none');
        document.getElementById('username-display').textContent = username;
    },
    
    updateTabStyles(clickedTab) {
        const allTabs = document.querySelectorAll('.nav-link');
        allTabs.forEach(tab => {
            if (tab === clickedTab) {
                tab.classList.add('bg-primary');
            } else {
                tab.classList.remove('bg-primary');
            }
        });
    }
};

// Validation Module
const ValidationModule = {
    rules: {
        username: {
            minLength: 3,
            maxLength: 150,
            defaultMessage: 'Enter your username',
            errorMessage: 'Username must be 3-150 characters'
        },
        password: {
            minLength: 6,
            maxLength: 128,
            defaultMessage: 'Enter your password',
            errorMessage: 'Password must be 6-128 characters'
        },
        confirm_password: {
            defaultMessage: 'Repeat your password',
            errorMessage: 'Passwords do not match'
        }
    },

    validateField(field, fieldName, isRegister = false) {
        const prefix = isRegister ? 'reg-' : '';
        const statusElement = document.getElementById(`${prefix}${fieldName}-status`);
        
        if (!statusElement || !field) return false;

        if (!field.value) {
            this.updateFieldStatus(field, statusElement, false, this.rules[fieldName].defaultMessage, true);
            return false;
        }

        let isValid = true;
        let message = 'Looks good!';

        if (fieldName === 'confirm_password') {
            const passwordField = document.getElementById(`${prefix}password`);
            isValid = field.value === passwordField.value;
            message = isValid ? message : this.rules[fieldName].errorMessage;
        } else {
            const rule = this.rules[fieldName];
            isValid = field.value.length >= rule.minLength && 
                     field.value.length <= (rule.maxLength || Number.MAX_SAFE_INTEGER);
            message = isValid ? message : rule.errorMessage;
        }

        this.updateFieldStatus(field, statusElement, isValid, message);
        return isValid;
    },

    updateFieldStatus(field, statusElement, isValid, message, isEmpty = false) {
        if (!field || !statusElement) return;

        field.classList.remove('is-valid', 'is-invalid');
        statusElement.classList.remove('text-success', 'text-danger', 'text-light', 'text-info');
        
        if (isEmpty) {
            statusElement.classList.add('text-light');
        } else if (isValid) {
            field.classList.add('is-valid');
            statusElement.classList.add('text-success');
        } else {
            field.classList.add('is-invalid');
            statusElement.classList.add('text-danger');
        }
        
        statusElement.textContent = message;
    }
};

// Form Module
const FormModule = {
    setupFormSubmit(formType, form) {
        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';

            try {
                const response = await fetch(`/${formType}/`, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: {
                        'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();

                if (response.ok) {
                    if (formType === 'register') {
                        // Realiza el inicio de sesión automáticamente
                        const loginResponse = await fetch('/login/', {
                            method: 'POST',
                            body: new URLSearchParams({
                                username: form.querySelector('[name="username"]').value,
                                password: form.querySelector('[name="password"]').value
                            }),
                            headers: {
                                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                                'X-Requested-With': 'XMLHttpRequest'
                            }
                        });

                        if (loginResponse.ok) {
                            const loginData = await loginResponse.json();
                            window.location.href = loginData.redirect || '/chat/';
                            return;
                        } else {
                            NotificationModule.showNotification(
                                'Login failed after registration. Please log in manually.',
                                'error',
                                5000
                            );
                            return;
                        }
                    }

                    // Para login directo
                    window.location.href = data.redirect || '/chat/';
                } else {
                    NotificationModule.showNotification(data.message || 'Invalid form submission', 'error', 5000);
                }
            } catch (error) {
                console.error('Error during form submission:', error);
                NotificationModule.showNotification('Connection error. Please try again.', 'error', 5000);
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = formType.toUpperCase();
            }
        });
    },
    
    clearForm(formId) {
        const form = document.getElementById(formId);
        if (!form) return;

        form.reset();
        const isLoginForm = formId === 'login-form';
        const prefix = isLoginForm ? '' : 'reg-';
        const fields = isLoginForm ? ['username', 'password'] : ['username', 'password', 'confirm_password'];

        fields.forEach(field => {
            const input = form.querySelector(`[name="${field}"]`);
            const status = document.getElementById(`${prefix}${field}-status`);
            if (input && status) {
                input.classList.remove('is-valid', 'is-invalid');
                status.classList.remove('text-danger', 'text-success');
                status.classList.add('text-light');
                status.textContent = ValidationModule.rules[field].defaultMessage;
            }
        });
    }
};

// Initialize everything
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm) FormModule.setupFormSubmit('login', loginForm);
    if (registerForm) FormModule.setupFormSubmit('register', registerForm);

    ['login-form', 'register-form'].forEach(formId => {
        const form = document.getElementById(formId);
        const isRegister = formId === 'register-form';
        
        if (form) {
            const fields = isRegister ? 
                ['username', 'password', 'confirm_password'] : 
                ['username', 'password'];

            fields.forEach(field => {
                const input = form.querySelector(`[name="${field}"]`);
                if (input) {
                    input.addEventListener('input', () => 
                        ValidationModule.validateField(input, field, isRegister)
                    );
                }
            });
        }
    });

    const tabs = document.querySelectorAll('[data-bs-toggle="tab"]');
    tabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', (e) => {
            UIModule.updateTabStyles(e.target);
        });
    });

    const activeTab = document.querySelector('.nav-link.active');
    if (activeTab) {
        UIModule.updateTabStyles(activeTab);
    }
});