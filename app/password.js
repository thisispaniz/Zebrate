document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('passwordInp');
    const submitBtn = document.getElementById('submitBtn');
    const checklist = {
        length: document.getElementById('length'),
        number: document.getElementById('number'),
        lowercase: document.getElementById('lowercase'),
        uppercase: document.getElementById('uppercase')
    };

    const validatePassword = () => {
        const password = passwordInput.value;
        let valid = true;

        if (password.length >= 8) {
            checklist.length.classList.add('valid');
        } else {
            checklist.length.classList.remove('valid');
            valid = false;
        }

        if (/\d/.test(password)) {
            checklist.number.classList.add('valid');
        } else {
            checklist.number.classList.remove('valid');
            valid = false;
        }

        if (/[a-z]/.test(password)) {
            checklist.lowercase.classList.add('valid');
        } else {
            checklist.lowercase.classList.remove('valid');
            valid = false;
        }

        if (/[A-Z]/.test(password)) {
            checklist.uppercase.classList.add('valid');
        } else {
            checklist.uppercase.classList.remove('valid');
            valid = false;
        }

        submitBtn.disabled = !valid;
    };

    passwordInput.addEventListener('input', validatePassword);
    
});

let showPasswordBtn = document.querySelector('.show-password');
let passwordInp = document.querySelector('.password-input');
let passwordChecklist = document.querySelectorAll('.list-item');

showPasswordBtn.addEventListener('click', () => {
    showPasswordBtn.classList.toggle('fa-eye');
    showPasswordBtn.classList.toggle('fa-eye-slash');

    passwordInp.type = (passwordInp.type === 'password') ? 'text' : 'password';
});