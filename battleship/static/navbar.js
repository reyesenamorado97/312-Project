// Burger Dropdown Functionality
const burgerIcon = document.querySelector("#burger");
const navbarMenu = document.querySelector("#nav-links");

// If we click of the burger, toggle the active state on/off
burgerIcon.addEventListener("click", () => {
	navbarMenu.classList.toggle("is-active");
});