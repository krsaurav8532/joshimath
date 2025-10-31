const toggleBtn = document.getElementById('menuToggle');
const menu = document.getElementById('menuList');

toggleBtn.addEventListener('click', () => {
    menu.classList.toggle('show');
});



const carouselSlide = document.getElementById('carouselSlide');
const images = carouselSlide.querySelectorAll('img');
let index = 0;

function showSlide(i) {
    index = (i + images.length) % images.length; // loop around
    carouselSlide.style.transform = `translateX(-${index * 100}vw)`;
}

function nextSlide() {
    showSlide(index + 1);
}

function prevSlide() {
    showSlide(index - 1);
}

// Auto-slide every 5 seconds
setInterval(() => {
    nextSlide();
}, 5000);

// Start with first slide
showSlide(0);

// Mobile menu toggle
const toggle = document.getElementById('menuToggle');
const menu = document.getElementById('menuList');
const dropdowns = document.querySelectorAll('.nav-item.dropdown');

toggle.addEventListener('click', () => {
    menu.classList.toggle('show');
});

// For mobile: click to open dropdown
dropdowns.forEach(item => {
    item.addEventListener('click', function (e) {
        if (window.innerWidth <= 768) {
            e.preventDefault();
            this.classList.toggle('open');
        }
    });
});
