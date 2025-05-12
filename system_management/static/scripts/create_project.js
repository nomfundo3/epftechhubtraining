
$(document).ready(function() {
    $(".update_submit").on("click", function (submit_event) {
        submit_event.preventDefault();        
        var project_id = $(this).attr('data-id')
        var name = $(`#name_${project_id}`).val();
        var description = $(`#description_${project_id}`).val();

        var data = {
            "project_id": project_id, 
            "name": name,
            "description": description,
            "csrfmiddlewaretoken": CSRF_TOKEN,
        }; 

        $.ajax({
            type: 'POST',
            url: UPDATE_PROJECT_URL,
            data: data,
            dataType: 'json',
            headers: {
                'Authorization': CSRF_TOKEN,
            },
            
            success: function (response) {
                if (response.status === "success") {
                    console.log(data['description'])
                    Swal.fire({
                        icon: 'success',
                        title: 'Project Updated',
                        text: 'The project has been successfully updated.'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.reload();
                        }
                    });
                } else {
                    
                }
            },
            error: function (response) {
                $("#successMessage").hide();
                $("#errorMessage").text("An error occurred. Please try again later.");
                $("#errorMessage").show();
            }
        });
    });

    $("#CreateProjectForm").submit(function(event) {
        event.preventDefault();
        var projectName = $("#projectName").val();
        var projectDescription = $("#projectDescription").val();
       
        projectData = {
            "name": projectName,
            "description": projectDescription,
            "csrfmiddlewaretoken": CSRF_TOKEN
        };


        $.ajax({
            url: PROJECTS_URL,
            type: 'POST',
            data: projectData,
            dataType: 'json',

          success: function(response) {
              if (response.status == "success") {
                  $("#successMessage").text("Project created successfully");
                  $("#successMessage").show();
                  $("#errorMessage").hide();
                  location.reload();
              } else {
                  $("#successMessage").hide();
                  $("#errorMessage").text("Failed to create project.");
                  $("#errorMessage").show();
              }
          },
          error: function() {
              $("#successMessage").hide();
              $("#errorMessage").text("An error occurred. Please try again later.");
              $("#errorMessage").show();
          }
      });
  });
  
          
    $('.delete_project_button').on("click", function() {
        var project_id = $(this).attr('data-project_id');
    
         Swal.fire({
             icon: 'warning',
             title: 'Are you sure you want to delete this project?',
             showCancelButton: true,
             confirmButtonText: 'Yes',
             cancelButtonText: 'No',
         }).then((result) => {  
    
             if (result.isConfirmed) {
                var data = {
                "project_id": project_id,
                'csrfmiddlewaretoken': CSRF_TOKEN
                    };
                    $.ajax({
                        data: data,
                        dataType: "json",
                        url: DELETE_PROJECT_URL,
                        type: "POST",
                        success: function(response) {
                            if (response.status == 'success') {
                                swal.fire({
                                    icon:'success',
                                    text:'Project deleted successfully'
                                }).then((result)=> {
                                    if(result.isConfirmed){
                                    window.location.reload();
                                    }
                                })

                            }  
                            else {
                                Swal.fire({
                                    icon: 'error',
                                    title: 'Error',
                                    text: 'An error occured while deleting the project',
                                    confirmButtonText: 'OK',
                                });
                            }
                        },
                    });
                 }
            });
    });

    $('.data-table').DataTable();
});
