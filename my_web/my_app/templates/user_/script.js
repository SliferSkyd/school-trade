document.addEventListener('DOMContentLoaded', function () {
    console.log('Script loaded');

    // Dữ liệu tĩnh
    const posts = [
        {
            id: 1,
            title: 'Áo khoác mùa thu',
            author: 'Nguyễn Thị Ánh Tuyết',
            type: 'Thanh lý',
            price: '250.000 VND',
            image: 'https://i.pinimg.com/736x/c3/de/c5/c3dec50c8063a844e0d960463ee620b9.jpg',
            description: 'Áo khoác ấm, chất liệu len cao cấp'
        },
        {
            id: 2,
            title: 'Máy tính Casio',
            author: 'Lương Gia Khánh',
            type: 'Trao đổi',
            image: 'https://i.pinimg.com/736x/c1/15/67/c1156779b5e6b747967911c23f71f006.jpg',
            description: 'Máy tính khoa học, còn mới 90%'
        },
        {
            id: 3,
            title: 'Bán sách cũ',
            author: 'Hoàng Thu Hiếu',
            type: 'Thanh lý',
            price: '100.000 VND',
            image: 'https://i.pinimg.com/736x/c3/de/c5/c3dec50c8063a844e0d960463ee620b9.jpg',
            description: 'Sách giáo khoa cũ, còn tốt'
        },
        {
            id: 4,
            title: 'Trao đổi máy tính',
            author: 'Hoàng Thu Hiếu',
            type: 'Trao đổi',
            image: 'https://i.pinimg.com/736x/c1/15/67/c1156779b5e6b747967911c23f71f006.jpg',
            description: 'Máy tính bỏ túi, hoạt động tốt'
        },
        {
            id: 5,
            title: 'Trao đổi điện thoại',
            author: 'Hoàng Thu Hiếu',
            type: 'Trao đổi',
            image: 'https://i.pinimg.com/736x/c1/15/67/c1156779b5e6b747967911c23f71f006.jpg',
            description: 'Điện thoại cũ, còn dùng được'
        }
    ];
    const events = [
        {
            id: 1,
            title: 'Sự kiện quyên góp cho trẻ em vùng lũ lụt',
            organizer: 'SGUET',
            type: 'Quyên góp',
            startDate: '12/5/2025',
            endDate: '12/6/2025',
            image: 'https://i.pinimg.com/736x/38/ff/3e/38ff3e465355367422ba9f0566c69f32.jpg'
        },
        {
            id: 2,
            title: 'Sự kiện gây quỹ tưởng niệm các anh hùng liệt sĩ',
            organizer: 'SGUET',
            type: 'Gây quỹ',
            startDate: '12/5/2025',
            endDate: '12/6/2025',
            image: 'https://i.pinimg.com/736x/70/57/1d/70571dca26c4d94854860857e6fe5fb6.jpg'
        },
        {
            id: 3,
            title: 'Gây quỹ thư viện',
            organizer: 'SGUET',
            type: 'Gây quỹ',
            startDate: '01/05/2025',
            endDate: '01/06/2025',
            image: 'https://i.pinimg.com/736x/38/ff/3e/38ff3e465355367422ba9f0566c69f32.jpg'
        },
        {
            id: 4,
            title: 'Tết thiện nguyện',
            organizer: 'SGUET',
            type: 'Quyên góp',
            startDate: '15/01/2025',
            endDate: '15/02/2025',
            image: 'https://i.pinimg.com/736x/70/57/1d/70571dca26c4d94854860857e6fe5fb6.jpg'
        }
    ];

    // Xử lý nút "Xem chi tiết"
    const buttons = document.querySelectorAll('.btn-primary');
    console.log('Buttons found:', buttons.length);

    buttons.forEach(button => {
        button.addEventListener('click', function () {
            const page = window.location.pathname.toLowerCase();
            const id = this.getAttribute('data-id');
            const type = this.getAttribute('data-type');
            console.log('Button clicked:', { page, id, type });

            if (page.includes('home.html') || page === '/home.html' || page === '/index.html' || page === '/' ||
                page.includes('profile.html') || page === '/profile.html' ||
                page.includes('group.html') || page === '/group.html') {
                if (type === 'post') {
                    window.location.href = `post.html?id=${id}`;
                } else if (type === 'event') {
                    window.location.href = `event.html?id=${id}`;
                }
            } else if (page.includes('post.html') || page === '/post.html') {
                showPostDetail(id);
            } else if (page.includes('event.html') || page === '/event.html') {
                showEventDetail(id);
            }
        });
    });

    // Xử lý nút "Quay lại"
    const backButtons = document.querySelectorAll('.btn-back');
    backButtons.forEach(button => {
        button.addEventListener('click', function () {
            console.log('Back button clicked');
            const postsSection = document.querySelector('.posts');
            const detailSection = document.querySelector('.detail-section');
            if (postsSection && detailSection) {
                postsSection.style.display = 'flex';
                detailSection.style.display = 'none';
            }
        });
    });

    // Xử lý hiển thị chi tiết bài đăng
    function showPostDetail(id) {
        const post = posts.find(p => p.id === parseInt(id));
        if (!post) {
            console.error('Post not found:', id);
            return;
        }
        console.log('Showing post:', post);

        const postsSection = document.querySelector('.posts');
        const detailSection = document.querySelector('.detail-section');
        if (postsSection && detailSection) {
            postsSection.style.display = 'none';
            detailSection.style.display = 'block';

            document.getElementById('post-title').textContent = post.title;
            document.getElementById('post-image').src = post.image;
            document.getElementById('post-author').textContent = `Người đăng: ${post.author}`;
            document.getElementById('post-type').textContent = `Loại bài: ${post.type}`;
            document.getElementById('post-price').textContent = post.price ? `Giá bán: ${post.price}` : 'Không có giá';
            document.getElementById('post-description').textContent = post.description || 'Không có mô tả';
        } else {
            console.error('Posts or detail section not found');
        }
    }

    // Xử lý hiển thị chi tiết sự kiện
    function showEventDetail(id) {
        const event = events.find(e => e.id === parseInt(id));
        if (!event) {
            console.error('Event not found:', id);
            return;
        }
        console.log('Showing event:', event);

        const postsSection = document.querySelector('.posts');
        const detailSection = document.querySelector('.detail-section');
        if (postsSection && detailSection) {
            postsSection.style.display = 'none';
            detailSection.style.display = 'block';

            document.getElementById('event-title').textContent = event.title;
            document.getElementById('event-image').src = event.image;
            document.getElementById('event-organizer').textContent = `Tổ chức: ${event.organizer}`;
            document.getElementById('event-type').textContent = `Loại sự kiện: ${event.type}`;
            document.getElementById('event-startDate').textContent = `Ngày tổ chức: ${event.startDate}`;
            document.getElementById('event-endDate').textContent = `Ngày kết thúc: ${event.endDate}`;
        } else {
            console.error('Posts or detail section not found');
        }
    }

    // Xử lý hiển thị chi tiết khi truy cập trực tiếp qua URL
    const page = window.location.pathname.toLowerCase();
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    if (id) {
        console.log('URL has id:', id);
        if (page.includes('post.html') || page === '/post.html') {
            showPostDetail(id);
        } else if (page.includes('event.html') || page === '/event.html') {
            showEventDetail(id);
        }
    }
});