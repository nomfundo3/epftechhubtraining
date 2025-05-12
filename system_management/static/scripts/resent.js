$(document).ready(function() {

    $('#resend_otp').on('click', function(event) {
        event.preventDefault();
        resend_otp();
    });

    function resend_otp() {
        data = {
            "csrfmiddlewaretoken": CSRF_TOKEN,
        }
        $.ajax({
            type: 'GET',
            url: RESEND_URL,
            data: data,
            dataType: 'json',
            success: function(response) {

                showSuccessMessage("New OTP sent")
            },
            error: function(response) {

                showErrorMessage("Dead link");

            },
        });

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
    }
})