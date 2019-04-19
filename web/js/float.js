var vertical;
window.onscroll = function() {myFunction()};
    var navbar = document.getElementById("navbar");
    var sticky = navbar.offsetTop;

function myFunction() {
if (window.pageYOffset >= sticky) {
    navbar.classList.remove("after");
    navbar.classList.add("sticky");
} else {
    navbar.classList.remove("sticky");
    navbar.classList.add("after");
}
}