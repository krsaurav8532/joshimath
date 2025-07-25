# joshimath
let currentIndex = 0;
const imageUrls = [
    {% for image in announcement.images.all %}
"{{ image.image.url }}"{% if not forloop.last %}, {% endif %}
{% endfor %}
    ];

function openLightbox(index) {
    currentIndex = index;
    document.getElementById('lightbox-img').src = imageUrls[currentIndex];
    document.getElementById('lightbox').classList.add('show');
}

function closeLightbox() {
    document.getElementById('lightbox').classList.remove('show');
}

function showPrevImage() {
    currentIndex = (currentIndex - 1 + imageUrls.length) % imageUrls.length;
    document.getElementById('lightbox-img').src = imageUrls[currentIndex];
}

function showNextImage() {
    currentIndex = (currentIndex + 1) % imageUrls.length;
    document.getElementById('lightbox-img').src = imageUrls[currentIndex];
}

document.getElementById('lightbox-left').addannouncementListener('click', function (e) {
    e.stopPropagation();
    showPrevImage();
});

document.getElementById('lightbox-right').addannouncementListener('click', function (e) {
    e.stopPropagation();
    showNextImage();
});

// Keyboard navigation
document.addannouncementListener('keydown', function (e) {
    if (!document.getElementById('lightbox').classList.contains('show')) return;

    if (e.key === 'ArrowRight') showNextImage();
    else if (e.key === 'ArrowLeft') showPrevImage();
    else if (e.key === 'Escape') closeLightbox();
});