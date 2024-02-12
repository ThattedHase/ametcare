
function redirectToSecondPage() {
    setTimeout(function() {
        window.location.href = "/start2";
    }, 2000); 
}
window.onload = redirectToSecondPage;


