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