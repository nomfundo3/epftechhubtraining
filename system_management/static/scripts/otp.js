$(document).ready(function() {

    $('.otp-field').on('input', function() {
        var maxLength = parseInt($(this).attr('maxlength'));
        var inputValue = $(this).val();

        if (inputValue.length >= maxLength) {
            $(this).next('.otp-field').focus();
        }
    });
    $('.otp-field').on('keydown', function(e) {
        if (e.keyCode === 8 && $(this).val() === '') { // Backspace key
            $(this).prev('.otp-field').focus();
        }
    });
    $('#validate').on('click', function(event) {
        event.preventDefault();
        validateOTP();
    });
    $('.otp-field').on('keypress', function(evt) {
        var charCode = (evt.which) ? evt.which : evt.keyCode;
        if (charCode > 31 && (charCode < 48 || charCode > 57)) {
            return false;
        }
    });

    function validateOTP() {
        var nonAlphabeticPattern = /^[^A-Za-z]+$/;
        var first = $("#first").val();
        var second = $("#second").val();
        var third = $("#third").val();
        var fourth = $("#fourth").val();
        var entered_otp = first + second + third + fourth;
        if (nonAlphabeticPattern.test(first) && nonAlphabeticPattern.test(second) && nonAlphabeticPattern.test(third) && nonAlphabeticPattern.test(fourth)) {
            if (entered_otp.length != 4 || !/^\d+$/.test(entered_otp)) {
                showMessage("Invalid OTP format. Please enter a 4-digit OTP.");
                resetOTPInputs();
                return;
            }
        } else {
            Swal.fire({
                icon: 'error',
                text: 'You cannot Input Alphabetic Characters',
            });
        }

        data = {
            otp: entered_otp,
            "csrfmiddlewaretoken": CSRF_TOKEN,
        }
        $.ajax({
            type: 'POST',
            url: OTP_URL,
            data: data,
            dataType: 'json',
            success: function(response) {
                window.location.href = response.redirect_url;

            },
            error: function(response) {
                showErrorMessage("Invalid OTP");
            },
        });
    }

    function showMessage(message) {
        Swal.fire({
            icon: 'warning',
            text: message,
        });
    }

    function showSuccessMessage(message) {
        Swal.fire({
            icon: 'success',
            text: message,
        });
    }

    function showErrorMessage(message) {
        Swal.fire({
            icon: 'error',
            text: message,
        });
    }

    function resetOTPInputs() {
        $('.inputs').val('');
        $('.inputs:first').focus();
    }
});