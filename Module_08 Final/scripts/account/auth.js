// Validation Module
const ValidationModule = {
    rules: {
        username: {
            minLength: 3,
            defaultMessage: 'Enter your username',
            errorMessage: 'Username too short'
        },
        password: {
            minLength: 6,
            defaultMessage: 'Enter your password',
            errorMessage: 'Password too short'
        },
        confirm_password: {
            defaultMessage: 'Repeat your password',
            errorMessage: 'Passwords do not match'
        }
    },

    updateFieldStatus(field, statusElement, isValid, message, isEmpty = false) {
        field.classList.remove('is-valid', 'is-invalid', 'border-success', 'border-danger');
        statusElement.classList.remove('text-success', 'text-danger', 'text-light', 'text-warning', 'text-info');
        
        if (isEmpty) {
            statusElement.classList.add('text-light');
        } else if (isValid) {
            field.classList.add('is-valid');
            statusElement.classList.add('text-info');
        } else {
            field.classList.add('is-invalid');
            statusElement.classList.add('text-danger');
        }
        
        statusElement.textContent = message;
    },

    validateLoginField(field, fieldName) {
        const statusElement = document.getElementById(`${fieldName}-status`);
        const rule = this.rules[fieldName];
        
        if (field.value.length === 0) {
            this.updateFieldStatus(field, statusElement, false, rule.defaultMessage, true);
            return false;
        }
        
        const isValid = field.value.length >= rule.minLength;
        this.updateFieldStatus(
            field, 
            statusElement, 
            isValid, 
            isValid ? 'Looks good!' : rule.errorMessage
        );
        return isValid;
    },

    validateRegisterField(field, fieldName) {
        const statusElement = document.getElementById(`reg-${fieldName}-status`);
        const rule = this.rules[fieldName];
        
        if (field.value.length === 0) {
            this.updateFieldStatus(field, statusElement, false, rule.defaultMessage, true);
            return false;
        }

        let isValid = true;
        let message = 'Looks good!';

        if (fieldName === 'confirm_password') {
            const passwordField = document.getElementById('reg-password');
            isValid = field.value === passwordField.value;
            message = isValid ? 'Looks good!' : rule.errorMessage;
        } else {
            isValid = field.value.length >= rule.minLength;
            message = isValid ? 'Looks good!' : rule.errorMessage;
        }

        this.updateFieldStatus(field, statusElement, isValid, message);
        return isValid;
    }
};

// UI Module
const UIModule = {
    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    },

    showLoggedIn(username) {
        document.getElementById('auth-forms-container').classList.add('d-none');
        document.getElementById('user-info').classList.remove('d-none');
        document.getElementById('username-display').textContent = username;
    },

    showLoggedOut() {
        document.getElementById('auth-forms-container').classList.remove('d-none');
        document.getElementById('user-info').classList.add('d-none');
        
        FormModule.clearForm('login-form');
        FormModule.clearForm('register-form');
        
        const loginTab = document.getElementById('login-tab');
        if (loginTab) {
            loginTab.classList.add('bg-primary');
            const registerTab = document.getElementById('register-tab');
            if (registerTab) {
                registerTab.classList.remove('bg-primary');
            }
            const tab = new bootstrap.Tab(loginTab);
            tab.show();
        }
    },

    updateTabStyles(clickedTab) {
        const tabs = document.querySelectorAll('.nav-link');
        tabs.forEach(tab => {
            if (tab === clickedTab) {
                tab.classList.add('bg-primary');
            } else {
                tab.classList.remove('bg-primary');
            }
        });
    }
};

// Form Module
const FormModule = {
    clearForm(formId) {
        const form = document.getElementById(formId);
        const isLoginForm = formId === 'login-form';
        const prefix = isLoginForm ? '' : 'reg-';
        
        form.reset();
        form.querySelectorAll('input').forEach(input => {
            input.classList.remove('is-valid', 'is-invalid', 'border-success', 'border-danger');
        });
        
        ['username', 'password', 'confirm_password'].forEach(field => {
            const statusElement = document.getElementById(`${prefix}${field}-status`);
            if (statusElement) {
                statusElement.classList.remove('text-danger', 'text-success', 'text-warning', 'text-info');
                statusElement.classList.add('text-light');
                statusElement.textContent = ValidationModule.rules[field].defaultMessage;
            }
        });
    },

    async handleFormSubmit(formType, form) {
        if (!form.checkValidity() || form.querySelectorAll('.is-invalid').length > 0) {
            NotificationModule.showNotification('Please check the form for errors', 'danger');
            return;
        }

        try {
            const formData = new FormData(form);
            const response = await fetch(`/${formType}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': UIModule.getCsrfToken()
                },
                credentials: 'same-origin'
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.status === 'success') {
                    NotificationModule.showNotification(
                        formType === 'login' ? 'Welcome back!' : 'Registration successful!', 
                        'success'
                    );
                    UIModule.showLoggedIn(data.username);
                } else {
                    this.handleFormErrors(data.errors, formType === 'login');
                    // Mostrar mensaje de error específico
                    if (data.errors.username) {
                        NotificationModule.showNotification(data.errors.username[0], 'warning');
                    } else if (data.errors.password) {
                        NotificationModule.showNotification(data.errors.password[0], 'warning');
                    }
                }
            } else {
                NotificationModule.showNotification('Server error occurred', 'danger');
                console.error('Form submission failed:', response.status);
            }
        } catch (error) {
            NotificationModule.showNotification('Connection error', 'danger');
            console.error('Form submission error:', error);
        }
    },

    handleFormErrors(errors, isLogin) {
        Object.entries(errors).forEach(([field, [errorMessage]]) => {
            const prefix = isLogin ? '' : 'reg-';
            const input = document.querySelector(`[name="${field}"]`);
            const status = document.getElementById(`${prefix}${field}-status`);
            
            if (input && status) {
                input.classList.add('is-invalid');
                status.textContent = errorMessage;
                status.classList.remove('text-light');
                status.classList.add('text-danger');
            }
        });
    }
};

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Set up form validation listeners
    const forms = {
        'login-form': ['username', 'password'],
        'register-form': ['username', 'password', 'confirm_password']
    };

    Object.entries(forms).forEach(([formId, fields]) => {
        const form = document.getElementById(formId);
        const isLoginForm = formId === 'login-form';
        
        if (form) {
            fields.forEach(field => {
                const input = form.querySelector(`[name="${field}"]`);
                if (input) {
                    input.addEventListener('input', () => {
                        if (isLoginForm) {
                            ValidationModule.validateLoginField(input, field);
                        } else {
                            ValidationModule.validateRegisterField(input, field);
                        }
                    });
                }
            });

            form.addEventListener('submit', (e) => {
                e.preventDefault();
                FormModule.handleFormSubmit(isLoginForm ? 'login' : 'register', form);
            });
        }
    });

    // Set up tab listeners
    const tabs = document.querySelectorAll('[data-bs-toggle="tab"]');
    tabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', (e) => UIModule.updateTabStyles(e.target));
    });

    // Initialize login tab as active
    const loginTab = document.getElementById('login-tab');
    if (loginTab) {
        UIModule.updateTabStyles(loginTab);
    }
});

// Notification Module
const NotificationModule = {
    showNotification(message, type = 'warning') {
        const container = document.getElementById('notification-container');
        if (!container) return;

        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.role = 'alert';
        
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        container.appendChild(alert);

        // Remover automáticamente después de 5 segundos
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);

        // Eliminar del DOM después de que termine la animación
        alert.addEventListener('closed.bs.alert', () => {
            alert.remove();
        });
    }
};