let offset = 10;
const loadMoreBtn = document.getElementById('loadMoreBtn');
const container = document.getElementById('announcement-container');

loadMoreBtn.addEventListener('click', () => {
    loadMoreBtn.disabled = true;
    loadMoreBtn.innerText = 'Loading...';

    fetch(`?offset=${offset}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => response.json())
        .then(data => {
            const announcements = data.announcements;

            if (announcements.length === 0) {
                loadMoreBtn.innerText = 'No More Announcements';
                loadMoreBtn.disabled = true;
                return;
            }

            announcements.forEach(a => {
                const col = document.createElement('div');
                col.className = 'col-12 col-md-6 col-lg-4 announcement-item';

                col.innerHTML = `
          <div class="announcement-card">
            <div class="announcement-title">${a.title}</div>
            <div class="announcement-date">${a.location}, ${a.date}</div>
            ${a.link ? `<div class="announcement-link"><a href="${a.link}" target="_blank">Know More</a></div>` : ''}
          </div>
        `;
                container.appendChild(col);
            });

            offset += 10;
            loadMoreBtn.disabled = false;
            loadMoreBtn.innerText = 'Load More';
        })
        .catch(err => {
            console.error(err);
            loadMoreBtn.innerText = 'Try Again';
            loadMoreBtn.disabled = false;
        });
});
