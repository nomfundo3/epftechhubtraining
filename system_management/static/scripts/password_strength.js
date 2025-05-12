//start check password strength function
var message_timeout;
var weak_password_confirm = false;
$("#password").keyup(function() {
    var password = $(this).val();
    var password_strength_element = $("#password-strength");
    var weak_password_message = $(".weak-password");
    var strongPasswordMessage = $(".strong-password");
    var medium_password_message = $(".medium-password");

    var medium_password_confirm = false;
    clearTimeout(message_timeout);
    var contains_alphabet = /[a-zA-Z]/.test(password);
    var contains_number = /\d/.test(password);
    var contains_specialChar = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]+/.test(password);
    if (password.length < 8) {
        password_strength_element.removeClass("d-none");
        weak_password_message.removeClass("d-none");
        strongPasswordMessage.addClass("d-none");
        medium_password_message.addClass("d-none");
        weak_password_confirm = true;
        medium_password_confirm = false;
    } else if (contains_alphabet && contains_number && contains_specialChar) {
        password_strength_element.removeClass("d-none");
        strongPasswordMessage.removeClass("d-none");
        weak_password_message.addClass("d-none");
        medium_password_message.addClass("d-none");
        weak_password_confirm = false;
        medium_password_confirm = false;
    } else {
        password_strength_element.removeClass("d-none");
        medium_password_message.removeClass("d-none");
        weak_password_message.addClass("d-none");
        strongPasswordMessage.addClass("d-none");
        weak_password_confirm = false;
        medium_password_confirm = true;
    }



    message_timeout = setTimeout(function() {
        password_strength_element.addClass("d-none");
    }, 3000000);
});

$('#validate').on('click', function(event) {
    event.preventDefault();
    var password = $('#password').val();
    var confirm_password = $('#confirm_password').val();
    if (password !== confirm_password) {
        Swal.fire({
            icon: 'error',
            title: 'Sorry...',
            text: "Passwords don't match",
        });
        return
    }
    if (weak_password_confirm == true) {
        Swal.fire({
            title: 'Your password is weak?',
            text: 'Do you want to keep it?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes',
            cancelButtonText: 'No'
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = DASHBOARD_URL;
            }
        })
    } else {
        window.location.href = DASHBOARD_URL;
    }
});