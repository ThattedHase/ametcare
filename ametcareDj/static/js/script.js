
function redirectToSecondPage() {
    setTimeout(function() {
        window.location.href = "http://127.0.0.1:8000/start2";
    }, 2000); 
}
window.onload = redirectToSecondPage;


