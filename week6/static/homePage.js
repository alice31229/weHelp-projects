
document.addEventListener("DOMContentLoaded", function () {
    let applyBtn = document.querySelector('.applyBtn');
    
    let formGoAhead = document.querySelector('#signup');
    applyBtn.addEventListener('click', function (evt){
        evt.preventDefault();

        let name = document.querySelector('#nameID').value;
        let username = document.querySelector('#usernameUpID').value;
        let password = document.querySelector('#passwordUpID').value;

        if (name == '' || username == '' || password == ''){
            alert("Please enter name, username and password.");
            return;
        };

        formGoAhead.submit();
        evt.target.submit();

    });
});
