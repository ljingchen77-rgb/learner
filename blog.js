let allPosts = [];
let activeCategory = '全部';
const listView = document.getElementById('post-list');
const contentView = document.getElementById('post-content');
const itemsContainer = document.getElementById('post-items');
const filterContainer = document.getElementById('category-filter');
const bodyContainer = document.getElementById('post-body');
const commentsContainer = document.getElementById('comments-container');
const backBtn = document.getElementById('back-btn');

fetch('posts/posts.json')
    .then(r => { if (!r.ok) throw new Error('文章列表加载失败'); return r.json(); })
    .then(posts => {
        allPosts = posts;
        renderCategories();
        renderPosts(posts);
        const params = new URLSearchParams(window.location.search);
        const postFile = params.get('post');
        if (postFile) loadPost(postFile);
    })
    .catch(err => { itemsContainer.innerHTML = '<p style="color:#e74c3c">\u26a0 ' + err.message + '</p>'; });

function renderCategories() {
    const cats = ['全部', ...new Set(allPosts.flatMap(p => p.categories))];
    if (cats.length <= 1) { filterContainer.style.display = 'none'; return; }
    cats.forEach(cat => {
        const tag = document.createElement('span');
        tag.className = 'category-tag' + (cat === '全部' ? ' active' : '');
        tag.textContent = cat;
        tag.onclick = () => filterByCategory(cat);
        filterContainer.appendChild(tag);
    });
}

function filterByCategory(cat) {
    activeCategory = cat;
    document.querySelectorAll('.category-tag').forEach(t => {
        t.classList.toggle('active', t.textContent === cat);
    });
    const filtered = cat === '全部' ? allPosts : allPosts.filter(p => p.categories.includes(cat));
    renderPosts(filtered);
}

function renderPosts(posts) {
    itemsContainer.innerHTML = '';
    if (posts.length === 0) {
        itemsContainer.innerHTML = '<p style="color:#999">该分类下暂无文章 \u270d\ufe0f</p>';
        return;
    }
    posts.forEach(post => {
        const item = document.createElement('div');
        item.className = 'post-item';
        item.innerHTML = '<h3><a href="?post=' + encodeURIComponent(post.file) + '">' + post.title + '</a></h3>' +
            '<div class="post-meta">' + post.date + ' ' + post.categories.map(c => '<span class="tag">' + c + '</span>').join('') + '</div>' +
            '<p class="post-summary">' + post.summary + '</p>';
        itemsContainer.appendChild(item);
    });
}

function loadPost(file) {
    listView.classList.add('hidden');
    contentView.classList.add('active');
    window.scrollTo(0, 0);
    fetch(file)
        .then(r => { if (!r.ok) throw new Error('文章加载失败'); return r.text(); })
        .then(md => {
            const title = md.split('\n')[0].replace(/^#\s*/, '');
            bodyContainer.innerHTML = marked.parse(md);
            document.title = title + ' \u00b7 刘靖臣';
            loadComments();
        })
        .catch(err => { bodyContainer.innerHTML = '<p style="color:#e74c3c">\u26a0 ' + err.message + '</p>'; });
}

function showListView() {
    contentView.classList.remove('active');
    listView.classList.remove('hidden');
    window.history.pushState({}, '', 'blog.html');
    document.title = '博客 \u00b7 刘靖臣';
    clearComments();
}

backBtn.addEventListener('click', function(e) { e.preventDefault(); showListView(); });
window.addEventListener('popstate', function() {
    var p = new URLSearchParams(window.location.search);
    var f = p.get('post');
    if (f) loadPost(f); else showListView();
});

function loadComments() {
    commentsContainer.innerHTML = '';
    var script = document.createElement('script');
    script.src = 'https://utteranc.es/client.js';
    script.setAttribute('repo', 'ljingchen77-rgb/learner');
    script.setAttribute('issue-term', 'pathname');
    script.setAttribute('theme', 'preferred-color-scheme');
    script.setAttribute('crossorigin', 'anonymous');
    script.async = true;
    commentsContainer.appendChild(script);
}

function clearComments() { commentsContainer.innerHTML = ''; }
