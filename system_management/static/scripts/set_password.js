$('#validate').on('click', function(event) {
    event.preventDefault();
    var password = $('#password').val();
    data = {
        "password": password,
        "csrfmiddlewaretoken": CSRF_TOKEN
    }
    $.ajax({
        type: 'POST',
        url: RESEND_URL,
        data: data,
        dataType: 'json',

        success: function(response) {

        },
        error: function(response) {
            if (response.status == 'error') {
                Swal.fire({
                    icon: 'error',
                    title: 'Sorry...',
                    text: 'An error occurred. Please try again later.'
                });
            }

        }
    });
})