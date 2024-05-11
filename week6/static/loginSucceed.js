// sign out
document.addEventListener("DOMContentLoaded", function () {
    // Get reference to the logout link and the logout form
    const logoutLink = document.getElementById("logoutLink");
    const logoutForm = document.getElementById("logoutForm");

    // Add click event listener to the logout link
    logoutLink.addEventListener("click", function(event) {
        // Prevent the default behavior of the link
        event.preventDefault();
        
        // Submit the logout form
        logoutForm.submit();
        event.target.submit();
    });
});



// create message
document.addEventListener("DOMContentLoaded", function () {
    let createMessageBtn = document.querySelector('.createMessageBtn');
    
    createMessageBtn.onclick = function(event) {
        event.preventDefault();

        let member_id = this.id;
        let message = document.querySelector('#messageID').value;
        let message_info = {'member_id': member_id,
                            'message': message};

        fetch('http://127.0.0.1:8000/createMessage',{
                method: 'post',
                body: JSON.stringify(message_info),
                headers: {
                    'Content-Type': 'application/json'
                }
        })
        .then(function (response){ 
            return response;
        })
        .then(function (result){
            try{
                let ok = result.ok;
                console.log(ok);
            }
            catch(e){
                console.log('error');
            }

        }, false);

        // Clear the input field and refresh the page
        document.querySelector('#messageID').value = "";
        window.location.reload();
    };
});


// check whether delete message or not

document.addEventListener("DOMContentLoaded", function () {


    // Attach event listener to the body and delegate to button clicks
    document.body.addEventListener("click", function(event) {
        event.preventDefault();

        if (event.target && event.target.classList.contains("deleteMessageBtn")) {
            
            let result = confirm('確定要刪除嗎？');
            if (result) {
                let targetIDs = event.target.id;
                let targetIDsList = targetIDs.substring(1, targetIDs.length - 1).split(', ');
                let message_id = parseInt(targetIDsList[0]).toString();
                let member_id = parseInt(targetIDsList[1]).toString();
                let message_info = {'message_id': message_id,
                                    'member_id': member_id};

                fetch('http://127.0.0.1:8000/deleteMessage',{
                    method: 'post',
                    body: JSON.stringify(message_info),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(function (response){ 
                    return response;
                })
                .then(function (result){
                    try{
                        let ok = result.ok;
                        console.log(ok);
                    }
                    catch(e){
                        console.log('error');
                    }
    
                }, false);
                
                window.location.reload();
    
            };
            
        };
    });
    
});