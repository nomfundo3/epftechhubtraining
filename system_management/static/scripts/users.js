$(document).ready(function() {
    $('#create_user').click(function(event) {
        event.preventDefault();
        $('#message').show();
       

        var first_name = $("#name").val();
        var last_name = $("#surname").val();
        var email = $("#email").val();
        var user_type = $("#userType").val();
        var phone_number = $("#number").val();
        
        if (!first_name || !last_name || !email || !user_type) {
            showErrorMessage("Please fill out all fields.");
            return;
        }
        if (!(email == "")) {
            if (!validateEmail(email)) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'email is incorrect!',
                })
                return
            }
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please enter your email address!',
            })
            return
        }
        
        var data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "user_type": user_type,
            "phone_number": phone_number,
            "csrfmiddlewaretoken": CSRF_TOKEN,
        };
        $.ajax({
            type: 'POST',
            url: USERS_URL,
            data: data,
            dataType: 'json',
            success: function(response) {
                if (response.status === "success") {
                    Swal.fire({
                        icon: 'success',
                        title: 'User Created',
                        text: 'The user has been successfully created.'
                    }).then((result) => {

                        if (result.isConfirmed) {
        
                            window.location.reload();                 
        
                        }
        
                    });
                   
                    $('#register_form')[0].reset();
                } else {
                    showErrorMessage('Failed to create user. Please try again.');
                }
            },
            error: function(error) {
                showErrorMessage('An error occurred. Please try again later.');
            },
        });
    });

    function showErrorMessage(message) {
        Swal.fire({
            icon: 'error',
            text: message,
        });
    }

    $('.delete_selected_user').on("click", function(event) {
        event.preventDefault();
        var user_id = $(this).val();
        Swal.fire({
            icon: 'warning',
            title: 'Are you sure you want to delete this user?',
            showCancelButton: true,
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
        }).then((result) => {  
            if (result.isConfirmed) {
                var data = {
                    user_id: user_id,
                    'csrfmiddlewaretoken': CSRF_TOKEN
                };
                $.ajax({
                    data: data,
                    dataType: "json",
                    url: DELETE_USER_URL,
                    type: "POST",
                    headers: {
                        'Authorization': 'Token ' + CSRF_TOKEN, // Assuming CSRF_TOKEN is the actual token value
                    },
                    success: function(response) {
                        if (response.status === "success") {
                            Swal.fire({
                                icon: 'success',
                                title: 'User deleted',
                                text: 'Successfully deleted this user',
                                confirmButtonText: 'OK',
                            }),
                            window.location.href = USERS_URL;
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Error',
                                text: 'An error occurred while deleting the user information',
                                confirmButtonText: 'OK',
                            });
                        }
                    },
                });
            }
        });
    });
    
});


function validateEmail(email){
    const res = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return res.test(String(email).toLocaleLowerCase());
}


function isNumber(evt) {
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    return true;
}


$(document).ready(function () {

    $('#form_update_modal').on('show.bs.modal', function (event) {

        var button = $(event.relatedTarget);
        var user_id = button.data('user-id');
        var first_name = button.data('first-name');
        var last_name = button.data('last-name');
        var email = button.data('user-email');
        var phone_number = button.data('phone-number');
       

        $('#user_id').val(user_id);
        $('#first_Name').val(first_name);
        $('#last_Name').val(last_name);
        $('#email_a').val(email);
        $('#number_update').val(phone_number);
        

    });

    $("#save").on("click",function(){
    
    var user_id = $("#user_id").val();
    var first_name = $("#first_Name").val();
    var last_name = $("#last_Name").val();
    var email = $("#email_a").val();
    var phone_number = $("#number_update").val();

    if (!first_name || !last_name || !email || !phone_number) {
        showErrorMessage("Please fill out all fields.");
        return;
    }
    if (!(email == "")) {
        if (!validateEmail(email)) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'email is incorrect!',
            })
            return
        }
    } else {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Please enter your email address!',
        })
        return
    }

    data = {
        "user_id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "csrfmiddlewaretoken": CSRF_TOKEN,
    }
    $.ajax({
        type: 'POST',
        url: UPDATE_USER,
        data: data,
        dataType: 'json',
        headers: {
            'Authorization': CSRF_TOKEN
        },
        success: function(response) {
            if (response.status === "success") {
                Swal.fire({
                    icon: 'success',
                    title: 'User Updated',
                    text: 'The user has been successfully Updated.',
                }).then((result) => {

                    if (result.isConfirmed) {
                        window.location.reload();                
                    }
                     else {
                                Swal.fire({
                                    icon: 'error',
                                    title: 'Error',
                                    text: 'An error occured while deleting the project',
                                    confirmButtonText: 'OK',
                                });
                            }
    
                })
        
            }
        }
    });

 });   
});



$('.data-table').DataTable();





