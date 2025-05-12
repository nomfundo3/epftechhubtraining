function addWord() {
    const formfield = document.getElementById("formfield");
    const wordList = document.getElementById("wordList");
    const formName = document.getElementById("formName");

    const newWordValue = formfield.value.trim();

    if (newWordValue !== "") {
        const listItem = document.createElement("li");
        listItem.textContent = newWordValue;

        listItem.addEventListener("click", function () {
            wordList.removeChild(listItem);  //this is to delete words that are clicked. This is to ensure that users can remove fields that they nolonger 
        });

        wordList.append(listItem);
        formfield.value = ""; // Clear the input field
    }
}

$(document).ready(function(){
    $('#addWordButton').on('click',function(){
        addWord();
    })

    const submitButton = document.getElementById("submitFormFields");
    submitButton.addEventListener("click", function () {
        const listItems = document.querySelectorAll("#wordList li");
        const listContent = [];

        listItems.forEach(function (item) {
            listContent.push(item.textContent);
        });

        data = {
            "formName" : formName,
            "listContent" : listContent,
            "csrfmiddlewaretoken":CSRF_TOKEN
    
        };
        $.ajax({
            type: 'POST',
            url: FORM_URL,
            data: data,
            dataType: 'json',
            success: function (response) {
                
                if (response.status == "success") {
                  
                    window.location.reload();
                } else {
              
                    Swal.fire({
                        icon: 'error',
                        title: 'Sorry...',
                        text: response.message
                    });
                }
            }
        })
    });
});
