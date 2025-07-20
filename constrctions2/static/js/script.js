// script.js

// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', () => {
    // Get the filter buttons
    const filterButtons = document.querySelectorAll('#portfolio-flters li');

    // Add event listeners to each filter button
    filterButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            // Get the filter value from the data-filter attribute
            const filterValue = event.target.getAttribute('data-filter');

            // Remove the "active" class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));

            // Add the "active" class to the clicked button
            event.target.classList.add('active');

            // Get all portfolio items
            const portfolioItems = document.querySelectorAll('.portfolio-item');

            // Loop through all portfolio items and check if they should be shown
            portfolioItems.forEach(item => {
                if (filterValue === '*' || item.classList.contains(filterValue.slice(1))) {
                    item.style.display = 'block'; // Show the item
                } else {
                    item.style.display = 'none'; // Hide the item
                }
            });
        });
    });
});
const form = document.querySelector('form');
form.addEventListener('submit', function() {
    const totalCostInput = document.getElementById('total-cost');
    totalCostInput.removeAttribute('readonly');  // Remove readonly to ensure value is submitted
});


////silder
//JavaScript of responsive navigation menu

const menuBtn = document.querySelector(".menu-btn");
const navegation = document.querySelector(".navegation");

menuBtn.addEventListener("click", () => {
  //si la clase "active" está presente la elimina, de lo contrario la añade
  menuBtn.classList.toggle("active");
  navegation.classList.toggle("active");
});

//JavaScript for video slider navegation
const btns = document.querySelectorAll(".nav-btn");
const slides = document.querySelectorAll(".video-slide");
const contents = document.querySelectorAll(".content");

var sliderNav = function (manual) {
  //button
  btns.forEach((btn) => {
    btn.classList.remove("active");
  });

  //video
  slides.forEach((slide) => {
    slide.classList.remove("active");
  });

  //content
  contents.forEach((content) => {
    content.classList.remove("active");
  });

  //button
  btns[manual].classList.add("active");
  //video
  slides[manual].classList.add("active");
  //content
  contents[manual].classList.add("active");
};

btns.forEach((btn, i) => {
  btn.addEventListener("click", () => {
    sliderNav(i);
  });
});
