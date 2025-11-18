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

if (navbar) {
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.08)';
        }
        
        lastScroll = currentScroll;
    });
}

// 移动菜单切换 - 侧边栏抽屉式
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navLinks = document.querySelector('.nav-links');
const navOverlay = document.querySelector('.nav-overlay');

function toggleMobileMenu() {
    if (!navLinks || !mobileMenuToggle) return;
    const isActive = navLinks.classList.contains('active');
    navLinks.classList.toggle('active');
    mobileMenuToggle.classList.toggle('active');
    if (navOverlay) {
        navOverlay.classList.toggle('active');
    }
    // 防止背景滚动
    document.body.style.overflow = isActive ? '' : 'hidden';
}

function closeMobileMenu() {
    if (!navLinks || !mobileMenuToggle) return;
    navLinks.classList.remove('active');
    mobileMenuToggle.classList.remove('active');
    if (navOverlay) {
        navOverlay.classList.remove('active');
    }
    document.body.style.overflow = '';
}

if (mobileMenuToggle && navLinks) {
    mobileMenuToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleMobileMenu();
    });
    
    // 点击遮罩层关闭菜单
    if (navOverlay) {
        navOverlay.addEventListener('click', closeMobileMenu);
    }
    
    // 点击菜单项后关闭菜单
    const navLinksItems = navLinks.querySelectorAll('a');
    navLinksItems.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });
    
    // ESC键关闭菜单
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navLinks.classList.contains('active')) {
            closeMobileMenu();
        }
    });
}

// FAQ 折叠/展开
const faqItems = document.querySelectorAll('.faq-item');

if (faqItems.length > 0) {
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (question) {
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
        }
    });
}

// 截图标签切换（仅在存在这些元素时执行）
const tabButtons = document.querySelectorAll('.tab-btn');
const screenshotItems = document.querySelectorAll('.screenshot-item');

if (tabButtons.length > 0 && screenshotItems.length > 0) {
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
}

// 返回顶部按钮
const backToTopButton = document.querySelector('.back-to-top');

if (backToTopButton) {
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
}

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
    // 确保页面可见（移除可能导致页面隐藏的样式）
    try {
        // 立即确保body可见
        if (document.body) {
            document.body.style.opacity = '1';
            document.body.style.visibility = 'visible';
            document.body.style.display = '';
        }
        
        // 可选：添加淡入动画（仅在需要时）
        // document.body.style.opacity = '0';
        // setTimeout(() => {
        //     document.body.style.transition = 'opacity 0.5s ease-in';
        //     document.body.style.opacity = '1';
        // }, 100);
    } catch (error) {
        // 如果出错，确保页面仍然可见
        console.error('页面初始化出错:', error);
        if (document.body) {
            document.body.style.opacity = '1';
            document.body.style.visibility = 'visible';
            document.body.style.display = '';
        }
    }

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
    if (e.key === 'Escape' && navLinks && navLinks.classList.contains('active')) {
        navLinks.classList.remove('active');
        if (mobileMenuToggle) {
            mobileMenuToggle.classList.remove('active');
        }
        if (navOverlay) {
            navOverlay.classList.remove('active');
        }
        document.body.style.overflow = '';
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
                let absolute = href.startsWith('http') ? href : (new URL(href, window.location.href)).href;
                
                // 如果是移动端（Android），且链接是下载链接，自动改为Android版本
                const ua = navigator.userAgent || '';
                const isAndroid = /android/i.test(ua);
                if (isAndroid && absolute.includes('download.py')) {
                    // 将 type 参数改为 android
                    if (absolute.includes('type=')) {
                        // 替换现有的 type 参数
                        absolute = absolute.replace(/[?&]type=[^&]*/, '');
                        // 确保有 ? 或 & 分隔符
                        if (absolute.includes('?')) {
                            absolute += '&type=android';
                        } else {
                            absolute += '?type=android';
                        }
                    } else {
                        // 添加 type 参数
                        if (absolute.includes('?')) {
                            absolute += '&type=android';
                        } else {
                            absolute += '?type=android';
                        }
                    }
                    __xt_log(`mobile detected, changed to android: ${absolute}`);
                }
                
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

