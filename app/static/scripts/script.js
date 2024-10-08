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

document.addEventListener("DOMContentLoaded", function() {
  const searchBtn = document.getElementById('search-btn');

  searchBtn.addEventListener('click', function() {
      const searchQuery = document.getElementById('search').value;
      const jobType = document.getElementById('job-type').value;

      // Build the search URL
      let url = `/search_results?query=${searchQuery}`;
      if (jobType) {
          url += `&job_type=${jobType}`;
      }
      window.location.href = url;
  });
});

document.addEventListener("DOMContentLoaded", function() {
  const jobApplicationForm = document.getElementById('jobApplicationForm');

  if (jobApplicationForm) {
      jobApplicationForm.addEventListener('submit', function(event) {
          const resumeInput = document.getElementById('resume');
          const file = resumeInput.files[0];

          if (!file || file.type !== 'application/pdf') {
              event.preventDefault();
              alert('Please upload a PDF resume.');
          }
      });
  }
});
