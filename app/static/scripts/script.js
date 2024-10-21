const toggleBtn = document.querySelector('.toggle-btn');
const dropdown = document.querySelector('.dropdown');
const toggleIcon = document.querySelector('.toggle-btn i');

toggleBtn.addEventListener('click', function () {
  dropdown.classList.toggle('open');

  const isOpen = dropdown.classList.contains('open');

  toggleIcon.classList = isOpen
    ? 'fa-solid fa-xmark'
    : 'fa-solid fa-bars';
});

document.addEventListener('DOMContentLoaded', function() {
	const yearSpan = document.getElementById('year');
    const currentYear = new Date().getFullYear();
    yearSpan.textContent = currentYear;
});
