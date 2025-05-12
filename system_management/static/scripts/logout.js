$(document).ready(function() {

    $('#logout_b').on('click', function() {
        Swal.fire({
            icon: 'warning',
            title: 'Are you sure you want to logout?',
            showCancelButton: true,
            confirmButtonText: 'Yes',
        }).then(function(result) {
            if (result.isConfirmed) {
                var data = {
                    'csrfmiddlewaretoken': CSRF_TOKEN
                }
                $.ajax({
                    url: LOGOUT_URL,
                    method: 'POST',
                    data: data,
                    success: function() {
                        window.location.href = LOGIN_URL;
                    },
                    error: function(error) {
                        Swal.fire({
                            title: 'Error',
                            text: 'Logout failed. Please try again.',
                            icon: 'error',
                            confirmButtonText: 'OK',
                        });
                    },
                });
            }
        });
    });
})