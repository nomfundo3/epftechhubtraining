$('#login').on('click',function(event){
    event.preventDefault();
   
    var username = $('#username').val()
    var password = $('#password').val()

    function validateEmail(username){
        const res = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
       return res.test(String(username).toLocaleLowerCase());
   }

   if (!(username== "")){
       if(!validateEmail(username)){
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
        "username" : username,
        "password" : password,
        "csrfmiddlewaretoken":CSRF_TOKEN

    }

    $.ajax({
        type: 'POST',
        url: LOGIN_URL,
        data: data,
        dataType: 'json',
        success: function (response) {
            
            if (response.status == "success") {
              
                window.location.href = OTP_URL;
            } else {
              
                Swal.fire({
                    icon: 'error',
                    title: 'Sorry...',
                    text: response.message
                });
            }
        },
        error: function (xhr, textStatus, errorThrown) {
           
            Swal.fire({
                icon: 'error',
                title: 'Sorry...',
                text: 'An error occurred. Please try again later.'
            });
        }
    });
})
