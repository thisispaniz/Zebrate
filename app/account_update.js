
    // Get the modals


    // Get the buttons that open the modals
    document.addEventListener('DOMContentLoaded', function() {
        var changeUsernameModal = document.getElementById("change-username-modal");
        var changeEmailModal = document.getElementById("change-email-modal");
        var changePasswordModal = document.getElementById("change-password-modal");
        var changeUsernameBtn = document.getElementById("change-username-btn");
        var changeEmailBtn = document.getElementById("change-email-btn");
        var changePasswordBtn = document.getElementById("change-password-btn");
        var saveUsernameBtn = document.getElementById("save-username-btn")
        var saveEmailBtn = document.getElementById("save-email-btn")
        var savePasswordBtn = document.getElementById("save-password-btn")
        var closeButtons = document.getElementsByClassName("close")
        console.log(changeUsernameBtn);
        
        function closeModal(modalElement) {
            if (modalElement) {
                modalElement.style.display = "none";
                window.location.reload();
            }
        }
        function closeModalnoRefresh(modalElement) {
            if (modalElement) {
                modalElement.style.display = "none";
            }
        }
        if(changeUsernameBtn) {
            changeUsernameBtn.onclick = function() {
                if (changeUsernameModal) {
                    changeUsernameModal.style.display = "block"
                }
            }
        }
        if(changeEmailBtn) {
            changeEmailBtn.onclick = function() {
                if (changeEmailModal) {
                    changeEmailModal.style.display = "block"
                }
            }
        }
        if(changePasswordBtn) {
            changePasswordBtn.onclick = function() {
                if (changePasswordModal) {
                    changePasswordModal.style.display = "block"
                }
            }
        }

        if (saveUsernameBtn) {
            saveUsernameBtn.onclick = function () {
                var newUsername = document.getElementById("new-username-input").value;
                fetch('/api/update_username', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: 'new_username=' + encodeURIComponent(newUsername)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update UI or take action on success
                        closeModal(changeUsernameModal);
                        
                    } else {
                        // Handle error scenario
                        alert("Failed to update username: " + data.message);
                    }
                    
                })
                .catch((error) => {
                    console.error('Error:', error)
                });
            }
        }
        if (saveEmailBtn) {
            saveEmailBtn.onclick = function () {
                var newEmail = document.getElementById("new-email-input").value;
                fetch('/api/update_email', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: 'new_email=' + encodeURIComponent(newEmail)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update UI or take action on success
                        closeModal(changeEmailModal);
                        
                    } else {
                        // Handle error scenario
                        alert("Failed to update email: " + data.message);
                    }
                    
                })
                .catch((error) => {
                    console.error('Error:', error)
                });
            }
        }
        if (savePasswordBtn) {
            savePasswordBtn.onclick = function () {
                var newPassword = document.getElementById("new-password-input").value;
                fetch('/api/update_password', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: 'new_password=' + encodeURIComponent(newPassword)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update UI or take action on success
                        closeModal(changePasswordModal);
                        
                    } else {
                        // Handle error scenario
                        alert("Failed to update password: " + data.message);
                    }
                    
                })
                .catch((error) => {
                    console.error('Error:', error)
                });
            }
        }
        for (var i = 0; i < closeButtons.length; i++) {
        closeButtons[i].onclick = function() {
            closeModalnoRefresh(this.parentElement.parentElement);
        }
    }
        window.onclick = function(event) {
            if (event.target == changeUsernameModal) {
                changeUsernameModal.style.display = "none";
            }
        }
    });
    

