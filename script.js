// ===== 暗色模式切换 =====
const toggleBtn = document.getElementById('dark-toggle');
const body = document.body;

// 自动检测系统暗色偏好
if (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    body.classList.add('dark-mode');
    toggleBtn.textContent = '☀️';
}

// 检查浏览器是否保存过主题偏好
if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark-mode');
    toggleBtn.textContent = '☀️';
}

toggleBtn.addEventListener('click', () => {
    body.classList.toggle('dark-mode');

    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
        toggleBtn.textContent = '☀️';
    } else {
        localStorage.setItem('theme', 'light');
        toggleBtn.textContent = '🌙';
    }
});

// ===== 打字机效果（仅首次会话播放）=====
const text = "核工程与核技术 · 托卡马克等离子体 EUV 辐射";
const el = document.getElementById('typewriter');

if (!sessionStorage.getItem('tw_shown')) {
    let i = 0;
    function typeWriter() {
        if (i < text.length) {
            el.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, 60);
        }
    }
    window.addEventListener('load', typeWriter);
    sessionStorage.setItem('tw_shown', 'true');
} else {
    el.textContent = text;
}
