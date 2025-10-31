// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// 导航栏背景变化
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.08)';
    }
    
    lastScroll = currentScroll;
});

// 移动菜单切换
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navLinks = document.querySelector('.nav-links');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileMenuToggle.classList.toggle('active');
    });
}

// FAQ 折叠/展开
const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    
    question.addEventListener('click', () => {
        const isActive = item.classList.contains('active');
        
        // 关闭所有其他项
        faqItems.forEach(otherItem => {
            if (otherItem !== item) {
                otherItem.classList.remove('active');
            }
        });
        
        // 切换当前项
        if (isActive) {
            item.classList.remove('active');
        } else {
            item.classList.add('active');
        }
    });
});

// 截图标签切换
const tabButtons = document.querySelectorAll('.tab-btn');
const screenshotItems = document.querySelectorAll('.screenshot-item');

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const targetTab = button.getAttribute('data-tab');
        
        // 更新按钮状态
        tabButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        
        // 更新截图显示
        screenshotItems.forEach(item => {
            if (item.getAttribute('data-content') === targetTab) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    });
});

// 返回顶部按钮
const backToTopButton = document.querySelector('.back-to-top');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTopButton.classList.add('visible');
    } else {
        backToTopButton.classList.remove('visible');
    }
});

backToTopButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// 交叉观察器 - 滚动动画
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// 为需要动画的元素添加初始样式和观察
const animateElements = document.querySelectorAll('.feature-card, .pain-point-card, .step, .faq-item');
animateElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(el);
});

// 统计数字动画
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value + '%';
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// 当统计数字进入视口时开始动画
const statObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
            entry.target.classList.add('animated');
            const targetValue = 90;
            animateValue(entry.target, 0, targetValue, 2000);
        }
    });
}, { threshold: 0.5 });

// 只对特定的统计数字应用动画
const statNumbers = document.querySelectorAll('.hero-stats .stat-number');
statNumbers.forEach(stat => {
    if (stat.textContent.includes('%')) {
        statObserver.observe(stat);
    }
});

// 下载按钮点击事件追踪
const downloadButtons = document.querySelectorAll('a[href*=".exe"], a[download]');
downloadButtons.forEach(button => {
    button.addEventListener('click', () => {
        console.log('下载按钮被点击');
        // 这里可以添加统计代码，如 Google Analytics
        // gtag('event', 'download', { 'event_category': 'engagement' });
    });
});

// 防止链接默认行为（对于占位符链接）
const placeholderLinks = document.querySelectorAll('a[href="#contact"], a[href="#feedback"], a[href="#about"], a[href="#privacy"], a[href="#terms"]');
placeholderLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        alert('此功能即将推出，敬请期待！');
    });
});

// 图片懒加载（如果浏览器不支持原生懒加载）
if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
        img.src = img.dataset.src;
    });
} else {
    // 使用 Intersection Observer 实现懒加载
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    const lazyImages = document.querySelectorAll('img.lazy');
    lazyImages.forEach(img => imageObserver.observe(img));
}

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', () => {
    // 添加页面加载动画
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in';
        document.body.style.opacity = '1';
    }, 100);

    // 自动打开第一个 FAQ（可选）
    // if (faqItems.length > 0) {
    //     faqItems[0].classList.add('active');
    // }

    // 不再需要 fetchLatestFileInfo，因为 download.py 会自动处理
});

// fetchLatestFileInfo 函数已移除，因为 download.py 会自动处理最新文件

// 性能监控
window.addEventListener('load', () => {
    // 计算页面加载时间
    const loadTime = performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart;
    console.log(`页面加载时间: ${loadTime}ms`);
});

// 处理表单提交（如果将来添加联系表单）
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        // 这里添加表单验证和提交逻辑
        console.log('表单已提交');
    });
});

// 键盘导航支持
document.addEventListener('keydown', (e) => {
    // ESC 键关闭移动菜单
    if (e.key === 'Escape' && navLinks.classList.contains('active')) {
        navLinks.classList.remove('active');
        mobileMenuToggle.classList.remove('active');
    }
});

// 添加键盘焦点可见性
document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-nav');
    }
});

document.addEventListener('mousedown', () => {
    document.body.classList.remove('keyboard-nav');
});

// 检测系统暗色模式（为未来的暗色模式做准备）
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    console.log('用户偏好暗色模式');
    // 可以在这里添加暗色模式逻辑
}

// 监听暗色模式变化
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    const darkModeOn = e.matches;
    console.log(`暗色模式: ${darkModeOn ? '开启' : '关闭'}`);
});

// 复制到剪贴板功能（用于未来可能的分享功能）
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text);
    } else {
        // 降级方案
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
        } catch (err) {
            console.error('复制失败:', err);
        }
        textArea.remove();
    }
}

// 导出函数供全局使用
window.xintuxiangce = {
    copyToClipboard,
    scrollToSection: (sectionId) => {
        const section = document.getElementById(sectionId);
        if (section) {
            const offsetTop = section.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    }
};

// 自动获取最新下载文件信息
async function updateDownloadInfo() {
    try {
        // 智能检测最新文件 - 尝试多个可能的文件名
        const possibleFiles = [
            'pc/portable/xtxc202510221247.zip',  // 最新便携版文件
            'pc/portable/xtxc202510151254.zip',  // 便携版备用文件
            'pc/portable/xtxc202510111614.zip',  // 便携版备用文件
            'pc/setup/xtxcsetup202510221247.zip',  // 安装版最新文件
            'pc/portable/芯图相册-智能分类，便捷管理，仅你可见 1.0.0.exe'  // 便携版exe文件作为最后备用
        ];
        
        let latestFile = null;
        
        // 尝试检测最新文件
        for (const filename of possibleFiles) {
            try {
                const response = await fetch(`dist/${filename}`, { method: 'HEAD' });
                if (response.ok) {
                    latestFile = {
                        filename: filename.split('/').pop(), // 只取文件名部分
                        path: `dist/${filename}`,
                        size: 315 * 1024 * 1024, // 最新文件大小
                        version: 'v1.0.1'
                    };
                    break;
                }
            } catch (e) {
                continue;
            }
        }
        
        // 如果没找到任何文件，使用默认的
        if (!latestFile) {
            latestFile = {
                filename: possibleFiles[0].split('/').pop(), // 只取文件名部分
                path: `dist/${possibleFiles[0]}`,
                size: 315 * 1024 * 1024,
                version: 'v1.0.1'
            };
        }
        
        // 更新所有下载按钮的链接（但不要覆盖指向版本选择页面、直接下载链接或CGI脚本的按钮）
        const downloadButtons = document.querySelectorAll('.download-btn');
        downloadButtons.forEach(btn => {
            // 如果按钮已经指向版本选择页面、直接下载链接或CGI脚本，不要覆盖
            if (btn.href.includes('download-select.html') || 
                btn.href.includes('dist/pc/portable/') || 
                btn.href.includes('dist/pc/setup/') ||
                btn.href.includes('.py') ||
                btn.closest('.hero-download-option')) {  // 不更新Hero区域的按钮
                return;
            }
            btn.href = latestFile.path;
            btn.download = latestFile.filename;
        });
        
        // 格式化文件大小
        const sizeFormatted = formatBytes(latestFile.size);
        
        // 更新页面上的文件信息
        const versionElement = document.getElementById('file-version');
        const versionElement2 = document.getElementById('file-version-2');
        const sizeElement = document.getElementById('file-size');
        const sizeElement2 = document.getElementById('file-size-2');
        
        if (versionElement) versionElement.textContent = latestFile.version;
        if (versionElement2) versionElement2.textContent = '版本 ' + latestFile.version;
        if (sizeElement) sizeElement.textContent = sizeFormatted;
        if (sizeElement2) sizeElement2.textContent = sizeFormatted;
        
        console.log('下载文件信息已更新:', latestFile);
    } catch (error) {
        console.error('获取下载文件信息失败:', error);
        // 如果获取失败，保持默认值
    }
}

// 格式化字节大小
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

console.log('芯图相册官网已加载完成 🎉');

// 调试工具：在微信或 ?debug=1 时在页面左下角显示日志
const __XT_VERSION = 'wx-intercept-20251030';
function __xt_shouldDebug() {
    try {
        const q = new URLSearchParams(location.search);
        if (q.get('debug') === '1') return true; // 仅当显式指定时显示调试面板
    } catch (e) {}
    return false;
}
function __xt_log(msg) {
    try {
        console.log('[XT]', msg);
        if (!__xt_shouldDebug()) return;
        let panel = document.getElementById('xt-debug-panel');
        if (!panel) {
            panel = document.createElement('div');
            panel.id = 'xt-debug-panel';
            panel.style.position = 'fixed';
            panel.style.left = '8px';
            panel.style.bottom = '8px';
            panel.style.maxWidth = '80vw';
            panel.style.maxHeight = '40vh';
            panel.style.overflow = 'auto';
            panel.style.background = 'rgba(0,0,0,0.7)';
            panel.style.color = '#0f0';
            panel.style.fontSize = '12px';
            panel.style.lineHeight = '1.4';
            panel.style.padding = '6px 8px';
            panel.style.borderRadius = '6px';
            panel.style.zIndex = '10000';
            panel.style.pointerEvents = 'none';
            panel.textContent = `[XT ${__XT_VERSION}]`;
            document.addEventListener('DOMContentLoaded', () => {
                document.body.appendChild(panel);
            });
            // 若 DOM 已就绪
            if (document.readyState !== 'loading' && document.body) {
                document.body.appendChild(panel);
            }
        }
        const line = document.createElement('div');
        const now = new Date();
        const ts = now.toLocaleTimeString();
        line.textContent = `${ts} - ${msg}`;
        panel.appendChild(line);
    } catch (e) {}
}
__xt_log('script loaded');

// 微信内置浏览器下载拦截与指引
(function () {
    try {
        const ua = navigator.userAgent || '';
        const isWeChat = ua.indexOf('MicroMessenger') !== -1;
        __xt_log(`UA=${ua}`);
        __xt_log(`isWeChat=${isWeChat}`);
        if (!isWeChat) return;

        const overlay = document.createElement('div');
        overlay.id = 'wx-download-overlay';
        overlay.style.position = 'fixed';
        overlay.style.left = '0';
        overlay.style.top = '0';
        overlay.style.right = '0';
        overlay.style.bottom = '0';
        overlay.style.background = 'rgba(0,0,0,0.65)';
        overlay.style.display = 'none';
        overlay.style.zIndex = '9999';
        overlay.style.backdropFilter = 'blur(2px)';

        const panel = document.createElement('div');
        panel.style.position = 'absolute';
        panel.style.left = '50%';
        panel.style.top = '50%';
        panel.style.transform = 'translate(-50%, -50%)';
        panel.style.width = 'min(92%, 560px)';
        panel.style.background = '#fff';
        panel.style.borderRadius = '12px';
        panel.style.boxShadow = '0 12px 32px rgba(0,0,0,0.2)';
        panel.style.padding = '20px 20px 16px';
        panel.style.textAlign = 'left';

        const title = document.createElement('div');
        title.textContent = '在微信内下载可能被拦截';
        title.style.fontSize = '18px';
        title.style.fontWeight = '600';
        title.style.color = '#111';
        title.style.marginBottom = '8px';

        const desc = document.createElement('div');
        desc.innerHTML = '请点击右上角 ···，选择“在浏览器中打开”后再进行下载；或复制下载链接到浏览器打开。';
        desc.style.fontSize = '14px';
        desc.style.color = '#444';
        desc.style.lineHeight = '1.6';
        desc.style.marginBottom = '14px';

        const input = document.createElement('input');
        input.type = 'text';
        input.readOnly = true;
        input.style.width = '100%';
        input.style.fontSize = '13px';
        input.style.padding = '10px 12px';
        input.style.border = '1px solid #e5e7eb';
        input.style.borderRadius = '8px';
        input.style.background = '#f9fafb';
        input.style.color = '#111';
        input.style.marginBottom = '12px';

        const actions = document.createElement('div');
        actions.style.display = 'flex';
        actions.style.gap = '10px';
        actions.style.justifyContent = 'flex-end';

        const copyBtn = document.createElement('button');
        copyBtn.textContent = '复制链接';
        copyBtn.style.padding = '10px 14px';
        copyBtn.style.border = '1px solid #2563eb';
        copyBtn.style.background = '#2563eb';
        copyBtn.style.color = '#fff';
        copyBtn.style.borderRadius = '8px';
        copyBtn.style.cursor = 'pointer';

        const closeBtn = document.createElement('button');
        closeBtn.textContent = '关闭';
        closeBtn.style.padding = '10px 14px';
        closeBtn.style.border = '1px solid #e5e7eb';
        closeBtn.style.background = '#fff';
        closeBtn.style.color = '#111';
        closeBtn.style.borderRadius = '8px';
        closeBtn.style.cursor = 'pointer';

        actions.appendChild(closeBtn);
        actions.appendChild(copyBtn);

        panel.appendChild(title);
        panel.appendChild(desc);
        panel.appendChild(input);
        panel.appendChild(actions);
        overlay.appendChild(panel);
        document.body.appendChild(overlay);

        let currentDownloadHref = '';

        function openOverlay(href) {
            currentDownloadHref = href;
            input.value = href;
            overlay.style.display = 'block';
            __xt_log('overlay open');
        }

        function closeOverlay() {
            overlay.style.display = 'none';
        }

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) closeOverlay();
        });
        closeBtn.addEventListener('click', closeOverlay);

        copyBtn.addEventListener('click', async () => {
            try {
                await (window.xintuxiangce && window.xintuxiangce.copyToClipboard
                    ? window.xintuxiangce.copyToClipboard(currentDownloadHref)
                    : navigator.clipboard.writeText(currentDownloadHref));
                copyBtn.textContent = '已复制';
                setTimeout(() => { copyBtn.textContent = '复制链接'; }, 1500);
            } catch (err) {
                console.error(err);
                copyBtn.textContent = '复制失败';
                setTimeout(() => { copyBtn.textContent = '复制链接'; }, 1500);
            }
        });

        // 拦截所有下载按钮（直链、download.py、dist 文件等）
        const candidates = document.querySelectorAll('a[href*="download.py"], a[href*="dist/"], a[href$=".exe"], a[href$=".zip"], a[href$=".apk"], a[download]');
        __xt_log(`candidates=${candidates.length}`);

        function interceptAnchor(a) {
            function handler(e) {
                const href = a.getAttribute('href') || '';
                if (!href) return;
                e.preventDefault();
                e.stopImmediatePropagation();
                const absolute = href.startsWith('http') ? href : (new URL(href, window.location.href)).href;
                openOverlay(absolute);
                __xt_log(`intercept: ${absolute}`);
                return false;
            }
            // 同时拦截 click 与 touchend，提升在微信内的可靠性
            a.addEventListener('click', handler, { capture: true });
            a.addEventListener('touchend', handler, { capture: true, passive: false });
            a.addEventListener('pointerup', handler, { capture: true });
        }

        candidates.forEach(interceptAnchor);
        __xt_log('bind done');
    } catch (e) {
        console.error('WeChat download intercept failed:', e);
        __xt_log('intercept init error');
    }
})();

