// not latest -> cmd + shift + R
// https://stackoverflow.com/questions/50371401/form-data-validation-before-submission

// main part for transit the form value from front-end input and validate it to the fastapi router
document.addEventListener("DOMContentLoaded", function () {
    let logInBtn = document.querySelector('.logInBtn');
    let checkbox = document.querySelector('#agreeID');
    let formGoAhead = document.querySelector('#signin');
    logInBtn.addEventListener('click', function (evt){
        evt.preventDefault();
        //let checkbox = document.querySelector('#agreeID').checked;

        if (!checkbox.checked){
            alert("Please check the checkbox first");
            return;
        };

        formGoAhead.submit();
        evt.target.submit();

    });
});


// optional task handling the positive input number
// alert shows up if non positive integer entered
function isPositiveInteger(value) {
    // Regular expression to match positive integers
    let pattern = /^[1-9]\d*$/;
    // Check if the value matches the pattern
    return pattern.test(value);
};

document.addEventListener("DOMContentLoaded", function () {
    let checkPositive = document.querySelector('.calculateBtn');
    let formGoAhead = document.querySelector('#square');
    checkPositive.addEventListener('click', function(evt) {
        evt.preventDefault();

        let inputValue = document.querySelector('#integerID').value;

        if (!isPositiveInteger(inputValue)) {
            alert("Please enter a positive number");
            return;
        };

        // Construct the URL dynamically
        const redirectUrl = `/square/${inputValue}`;

        // Redirect to the calculated URL
        formGoAhead.setAttribute('action', redirectUrl)

        formGoAhead.submit();
        evt.target.submit();
    });
});
