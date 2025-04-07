
document.addEventListener("DOMContentLoaded", function() {
	const menuIcon = document.getElementById("menuIcon");
	const navLinks = document.getElementById("navLinks");

	function toggleMenu() {
		console.log("Menu clicked!");
		navLinks.classList.toggle("active");
	}


	menuIcon.addEventListener("click", toggleMenu);
});