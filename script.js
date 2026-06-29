// ===== 暗色模式切换 =====
const toggleBtn = document.getElementById('dark-toggle');
const body = document.body;

// 自动检测系统暗色偏好（仅首次访问）
if (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    body.classList.add('dark-mode');
    toggleBtn.textContent = '\u2600\ufe0f';
}

// 检查浏览器是否保存过主题偏好
if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark-mode');
    toggleBtn.textContent = '\u2600\ufe0f';
}

toggleBtn.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
        toggleBtn.textContent = '\u2600\ufe0f';
    } else {
        localStorage.setItem('theme', 'light');
        toggleBtn.textContent = '\U0001F319';
    }
});

// ===== 打字机效果（仅首次会话播放）=====
const text = "核工程与核技术 \u00b7 核能科学与技术";
const el = document.getElementById('home-tagline');

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
