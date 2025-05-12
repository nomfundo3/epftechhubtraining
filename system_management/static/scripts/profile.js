function isNumber(evt) {

    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    return true;
}

$(document).ready(function() {

  

    $('#update-profile').on('click', function(event) {
        updateProfile();
    });

    function updateProfile() {
        const firstName = $("#first_Name").val();
        const lastName = $("#last_Name").val();
        const email = $("#email").val();
        const phoneNumber = $("#phone_Number").val();
        const gender = $("#gender").val();
        const identity_number = $("#identity_number").val();
        const passport = $("#passport_number").val();
        const date_of_birth = $("#date_of_birth").val();
        const ethnicity = $("#ethnicity").val();
        const address = $("#address").val();
        



        if (!firstName || !lastName || !email || !phoneNumber || !gender) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please fill in all the required fields.',
            })
            return;
        }

    data = {
        email: email,
        first_name: firstName,
        last_name: lastName,
        phone_number: phoneNumber,
        gender: gender,
        identity_number:identity_number,
        passport_number:passport,
        date_of_birth:date_of_birth,
        address:address,
        ethnicity:ethnicity,
        "csrfmiddlewaretoken": CSRF_TOKEN,
    };

        $.ajax({
            type: 'POST',
            url: PROFILE_URL,
            data: data,
            dataType: 'json',
            success: function(response) {
                if (response.status == "success") {
                    Swal.fire({
                        icon: 'success',
                        text: 'profile  successfully updated'

                    }).then((result) => {

                        if (result.isConfirmed) {

                            window.location.reload()

                        }

                    })

                }
            },
            error: function(response) {
                Swal.fire({
                    icon: 'error',
                    text: 'An error occured. Please try again later'
                });
            }
        })
    }

});